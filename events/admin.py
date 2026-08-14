from django.contrib import admin

from .models import (
    Customer,
    EventType,
    Event,
    CateringRequirement,
    ServiceArea,
    Venue,
    Quote,
    QuoteItem,
    ServicePricing,
    QuoteRequest,
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
        "email",
        "city",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    list_filter = (
        "city",
        "created_at",
    )


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "event_name",
        "customer",
        "event_type",
        "venue",
        "event_date",
        "venue_name",
        "city",
        "number_of_guests",
        "status",
    )

    list_filter = (
        "event_type",
        "status",
        "city",
    )

    search_fields = (
        "event_name",
        "venue_name",
        "city",
        "venue_address",
        "venue__name",
    )

    date_hierarchy = "event_date"


@admin.register(CateringRequirement)
class CateringRequirementAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "service_style",
        "number_of_servers",
        "setup_required",
        "cleanup_required",
        "tableware_required",
        "equipment_required",
        "budget_range",
    )

    list_filter = (
        "service_style",
        "setup_required",
        "cleanup_required",
        "tableware_required",
        "equipment_required",
        "budget_range",
    )

    search_fields = (
        "event__event_name",
        "event__customer__first_name",
        "event__customer__last_name",
        "dietary_requirements",
        "special_requests",
    )


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "region",
        "base_travel_fee",
        "setup_fee",
        "is_active",
    )

    list_filter = (
        "region",
        "is_active",
    )

    search_fields = (
        "name",
        "region",
        "description",
    )


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "service_area",
        "is_active",
    )

    list_filter = (
        "service_area",
        "city",
        "is_active",
    )

    search_fields = (
        "name",
        "address",
        "city",
    )


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1
    readonly_fields = ("amount",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "quote_number",
        "event",
        "quote_date",
        "valid_until",
        "subtotal",
        "travel_charge",
        "setup_charge",
        "cleanup_charge",
        "discount",
        "tax",
        "total",
        "status",
    )

    list_filter = (
        "status",
        "quote_date",
        "valid_until",
    )

    search_fields = (
        "quote_number",
        "event__event_name",
        "event__customer__first_name",
        "event__customer__last_name",
    )

    readonly_fields = (
        "quote_date",
    )

    inlines = [QuoteItemInline]


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = (
        "quote",
        "description",
        "quantity",
        "unit_price",
        "amount",
    )

    search_fields = (
        "description",
        "quote__quote_number",
        "quote__event__event_name",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "amount",
    )
@admin.register(ServicePricing)
class ServicePricingAdmin(admin.ModelAdmin):

    list_display = (
        "service_style",
        "price_per_guest",
        "minimum_guests",
        "active",
        )

    list_filter = (
        "service_style",
        "active",
        )

    search_fields = (
        "service_style",
        "description",
        )
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "event_type",
        "event_date",
        "guest_count",
        "service_style",
        "service_area",
        "estimated_total",
        "status",
        "created_at",
        )

    list_filter = (
        "status",
        "event_type",
        "service_style",
        "service_area",
        "event_date",
        )

    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "customer__phone",
        "dietary_requirements",
        "special_requests",
        )

    readonly_fields = (
        "created_at",
        "updated_at",
        )

    ordering = (
        "-created_at",
        )