from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, User

gender = [("M", "Male"), ("F", "Female")]
unit = [('microgram', "mcg"), ('milligram', "mg"), ('gram', "g"), ('kilo-calorie', "kcal"), ('litres', 'l')]


class UserTable(models.Model):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=50, null=False, blank=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    password = models.CharField(max_length=32, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    class Meta:
        db_table = "UsersTable"
        verbose_name = "Registered Users Table"


class UserFamilyMember(models.Model):
    user = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=50, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(choices=gender, max_length=10)
    pregnant = models.BooleanField(default=False)
    breastfeeding = models.BooleanField(default=False)


class NutrientsListTable(models.Model):
    nutrient = models.CharField(primary_key=True, max_length=30)
    nutrient_name = models.CharField(verbose_name="Nutrient Name",  max_length=20)
    nutrient_type = models.CharField(verbose_name="Nutrient Type",  max_length=20, blank=True)
    group = models.CharField(max_length=20, blank=True)
    benifits = models.TextField(verbose_name="Benifits", null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "Nutrients"
        verbose_name = "Nutrients List Table"


class DataTable(models.Model):
    nutrient = models.ForeignKey(NutrientsListTable, on_delete=models.CASCADE, max_length=30)
    nutrient_name = models.CharField(max_length=50)
    gender = models.CharField(choices=gender, max_length=10)
    pregnant = models.BooleanField(default=False)
    breastfeeding = models.BooleanField(default=False)
    age = models.PositiveIntegerField()
    nutrition_value = models.FloatField(validators=[MinValueValidator(0.0)])
    unit = models.CharField(max_length=20, choices=unit)
    last_update = models.DateTimeField(auto_now=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "Data_Table"
        verbose_name = "Data Table"


class DailyAllowanceSheet(models.Model):
    nutrient = models.ForeignKey(NutrientsListTable, on_delete=models.CASCADE, max_length=30, null=True, default=None)
    nutrient_name = models.CharField(max_length=100)
    f_0_6m = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F 0-.5", name='f_0_6m')
    m_0_6m = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M 0-.5", name='m_0_6m')
    f_6m_1 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F .5-1", name='f_6m_1')
    m_6m_1 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M .5-1", name='m_6m_1')
    f_1_3 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F 1-3", name='f_1_3')
    m_1_3 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M 1-3", name='m_1_3')
    f_4_8 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F 4-8", name='f_4_8')
    m_4_8 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M 4-8", name='m_4_8')
    f_9_13 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F 9-13", name='f_9_13')
    m_9_13 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M 9-13", name='m_9_13')
    f_14_18 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F 14-18", name='f_14_18')
    m_14_18 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M 14-18", name='m_14_18')
    f_19_50 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F 19-50", name='f_19_50')
    m_19_50 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M 19-50", name='m_19_50')
    f_50 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="F 50+", name='f_50')
    m_50 = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="M 50+", name='m_50')
    breastfeeding = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    pregnant = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    maximum_doses = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, verbose_name="Max doses M+F", name='maximum_doses')
    unit = models.CharField(max_length=20, choices=unit)
    last_update = models.DateTimeField(auto_now=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "Daily_Allowance_Sheet"
        verbose_name = "Daily Allowance Sheet"
