from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=30)

    alternative_phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    additional_information = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EventType(models.Model):
    name = models.CharField(max_length=100)

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):

    STATUS_CHOICES = [
        ("inquiry", "Inquiry"),
        ("quoted", "Quote Sent"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="events",
        blank=True,
        null=True
    )

    event_type = models.ForeignKey(
        EventType,
        on_delete=models.PROTECT,
        related_name="events"
    )

    venue = models.ForeignKey(
        "Venue",
        on_delete=models.PROTECT,
        related_name="events",
        blank=True,
        null=True
    )

    event_name = models.CharField(
        max_length=200,
        blank=True
    )

    event_date = models.DateField()

    start_time = models.TimeField(
        blank=True,
        null=True
    )

    end_time = models.TimeField(
        blank=True,
        null=True
    )

    venue_name = models.CharField(
        max_length=200
    )

    venue_address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    number_of_guests = models.PositiveIntegerField()

    event_description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="inquiry"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["event_date"]

    def __str__(self):
        if self.event_name:
            return f"{self.event_name} - {self.event_date}"

        return f"{self.event_type.name} - {self.event_date}"


class CateringRequirement(models.Model):

    SERVICE_STYLE_CHOICES = [
        ("buffet", "Buffet"),
        ("plated", "Plated Service"),
        ("finger_foods", "Cocktail / Finger Foods"),
        ("family_style", "Family Style"),
        ("packed_meals", "Packed Meals"),
        ("custom", "Custom"),
    ]

    BUDGET_RANGE_CHOICES = [
        ("under_500", "Under 500"),
        ("500_1000", "500 - 1,000"),
        ("1000_2500", "1,000 - 2,500"),
        ("2500_5000", "2,500 - 5,000"),
        ("5000_10000", "5,000 - 10,000"),
        ("over_10000", "Over 10,000"),
        ("not_specified", "Not Specified"),
    ]

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="catering_requirement"
    )

    service_style = models.CharField(
        max_length=30,
        choices=SERVICE_STYLE_CHOICES
    )

    number_of_servers = models.PositiveIntegerField(
        default=0
    )

    setup_required = models.BooleanField(
        default=False
    )

    cleanup_required = models.BooleanField(
        default=False
    )

    tableware_required = models.BooleanField(
        default=False
    )

    equipment_required = models.BooleanField(
        default=False
    )

    dietary_requirements = models.TextField(
        blank=True
    )

    special_requests = models.TextField(
        blank=True
    )

    budget_range = models.CharField(
        max_length=30,
        choices=BUDGET_RANGE_CHOICES,
        default="not_specified"
    )

    additional_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Catering Requirement"
        verbose_name_plural = "Catering Requirements"

    def __str__(self):
        return f"Catering Requirements - {self.event}"
class ServiceArea(models.Model):

    name = models.CharField(
        max_length=100
    )

    region = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    base_travel_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    setup_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
class Venue(models.Model):

    service_area = models.ForeignKey(
        ServiceArea,
        on_delete=models.PROTECT,
        related_name="venues"
    )

    name = models.CharField(
        max_length=200
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True
    )

    additional_information = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.city}"
class Quote(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    ]

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="quote"
    )

    quote_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    quote_date = models.DateField(
        auto_now_add=True
    )

    valid_until = models.DateField(
        blank=True,
        null=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    travel_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    setup_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    cleanup_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.quote_number} - {self.event}"
class QuoteItem(models.Model):

    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        related_name="items"
    )

    description = models.CharField(
        max_length=255
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.quote.quote_number}"    
