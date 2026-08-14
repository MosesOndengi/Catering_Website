from decimal import Decimal

from django.shortcuts import render
from django.db.models import Q

from .models import ServicePricing, ServiceArea


def estimator(request):
    estimate = None
    error = None

    pricing_options = ServicePricing.objects.filter(active=True)
    service_areas = ServiceArea.objects.filter(is_active=True)

    if request.method == "POST":

        try:
            service_style = request.POST.get("service_style")
            guest_count = int(request.POST.get("guest_count", 0))
            service_area_id = request.POST.get("service_area")
            setup_required = request.POST.get("setup_required") == "yes"
            cleanup_required = request.POST.get("cleanup_required") == "yes"

            if guest_count <= 0:
                raise ValueError("Guest count must be greater than zero.")

            pricing = ServicePricing.objects.get(
                service_style=service_style,
                active=True
            )

            if guest_count < pricing.minimum_guests:
                raise ValueError(
                    f"The minimum number of guests for this service is "
                    f"{pricing.minimum_guests}."
                )

            base_cost = (
                Decimal(guest_count) *
                pricing.price_per_guest
            )

            travel_charge = Decimal("0.00")
            setup_charge = Decimal("0.00")
            cleanup_charge = Decimal("0.00")

            if service_area_id:
                service_area = ServiceArea.objects.get(
                    id=service_area_id,
                    is_active=True
                )

                travel_charge = service_area.base_travel_fee

                if setup_required:
                    setup_charge = service_area.setup_fee

            if cleanup_required:
                cleanup_charge = Decimal("0.00")

            subtotal = (
                base_cost
                + travel_charge
                + setup_charge
                + cleanup_charge
            )

            # Estimate range: approximately +/- 10%
            lower_estimate = subtotal * Decimal("0.90")
            upper_estimate = subtotal * Decimal("1.10")

            estimate = {
                "service_style": pricing.get_service_style_display(),
                "guest_count": guest_count,
                "base_cost": base_cost,
                "travel_charge": travel_charge,
                "setup_charge": setup_charge,
                "cleanup_charge": cleanup_charge,
                "subtotal": subtotal,
                "lower_estimate": lower_estimate,
                "upper_estimate": upper_estimate,
            }

        except (ValueError, TypeError, ServicePricing.DoesNotExist):
            error = "Please check the information you entered and try again."

        except ServiceArea.DoesNotExist:
            error = "The selected service area is not available."

    context = {
        "pricing_options": pricing_options,
        "service_areas": service_areas,
        "estimate": estimate,
        "error": error,
    }

    return render(
        request,
        "events/estimator.html",
        context
    )