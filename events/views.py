from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import (
    Customer,
    EventType,
    ServicePricing,
    ServiceArea,
    QuoteRequest,
)


def estimator(request):

    estimate = None
    error = None

    pricing_options = ServicePricing.objects.filter(
        active=True
    )

    service_areas = ServiceArea.objects.filter(
        is_active=True
    )

    event_types = EventType.objects.filter(
        is_active=True
    )

    if request.method == "POST":

        try:
            action = request.POST.get("action")

            service_style = request.POST.get(
                "service_style"
            )

            guest_count = int(
                request.POST.get(
                    "guest_count",
                    0
                )
            )

            service_area_id = request.POST.get(
                "service_area"
            )

            setup_required = (
                request.POST.get(
                    "setup_required"
                ) == "yes"
            )

            cleanup_required = (
                request.POST.get(
                    "cleanup_required"
                ) == "yes"
            )

            equipment_required = (
                request.POST.get(
                    "equipment_required"
                ) == "yes"
            )

            tableware_required = (
                request.POST.get(
                    "tableware_required"
                ) == "yes"
            )

            pricing = ServicePricing.objects.get(
                service_style=service_style,
                active=True
            )

            if guest_count <= 0:
                raise ValueError(
                    "Guest count must be greater than zero."
                )

            if guest_count < pricing.minimum_guests:
                raise ValueError(
                    f"Minimum guests for this service "
                    f"is {pricing.minimum_guests}."
                )

            service_area = ServiceArea.objects.get(
                id=service_area_id,
                is_active=True
            )

            base_cost = (
                Decimal(guest_count)
                * pricing.price_per_guest
            )

            travel_charge = (
                service_area.base_travel_fee
            )

            setup_charge = Decimal("0.00")

            if setup_required:
                setup_charge = service_area.setup_fee

            cleanup_charge = Decimal("0.00")

            equipment_charge = Decimal("0.00")

            if equipment_required:
                equipment_charge = Decimal("100.00")

            tableware_charge = Decimal("0.00")

            if tableware_required:
                tableware_charge = Decimal(
                    guest_count
                ) * Decimal("2.00")

            subtotal = (
                base_cost
                + travel_charge
                + setup_charge
                + cleanup_charge
                + equipment_charge
                + tableware_charge
            )

            lower_estimate = (
                subtotal * Decimal("0.90")
            )

            upper_estimate = (
                subtotal * Decimal("1.10")
            )

            estimate = {
                "service_style":
                    pricing.get_service_style_display(),

                "guest_count":
                    guest_count,

                "base_cost":
                    base_cost,

                "travel_charge":
                    travel_charge,

                "setup_charge":
                    setup_charge,

                "cleanup_charge":
                    cleanup_charge,

                "equipment_charge":
                    equipment_charge,

                "tableware_charge":
                    tableware_charge,

                "subtotal":
                    subtotal,

                "lower_estimate":
                    lower_estimate,

                "upper_estimate":
                    upper_estimate,
            }

            # Formal quote request
            if action == "request_quote":

                customer, created = Customer.objects.get_or_create(
                    email=request.POST.get("email"),
                    defaults={
                        "first_name": request.POST.get(
                            "first_name"
                        ),
                        "last_name": request.POST.get(
                            "last_name"
                        ),
                        "phone": request.POST.get(
                            "phone"
                        ),
                        "city": request.POST.get(
                            "city",
                            ""
                        ),
                    }
                )

                event_type = EventType.objects.get(
                    id=request.POST.get(
                        "event_type"
                    )
                )

                QuoteRequest.objects.create(
                    customer=customer,
                    event_type=event_type,
                    event_date=request.POST.get(
                        "event_date"
                    ),
                    guest_count=guest_count,
                    service_style=service_style,
                    service_area=service_area,
                    setup_required=setup_required,
                    cleanup_required=cleanup_required,
                    equipment_required=equipment_required,
                    tableware_required=tableware_required,
                    dietary_requirements=request.POST.get(
                        "dietary_requirements",
                        ""
                    ),
                    special_requests=request.POST.get(
                        "special_requests",
                        ""
                    ),
                    estimated_total=subtotal,
                )

                messages.success(
                    request,
                    "Thank you! Your quote request has been received. "
                    "Our catering team will review your requirements "
                    "and contact you with a formal quotation."
                )

                return redirect(
                    "estimator"
                )

        except (
            ValueError,
            TypeError,
            ServicePricing.DoesNotExist,
            ServiceArea.DoesNotExist,
            EventType.DoesNotExist,
        ) as exc:

            error = str(exc)

    context = {
        "pricing_options": pricing_options,
        "service_areas": service_areas,
        "event_types": event_types,
        "estimate": estimate,
        "error": error,
    }

    return render(
        request,
        "events/estimator.html",
        context
    )