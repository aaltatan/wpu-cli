import peewee as models


db = models.SqliteDatabase("app.db")


class BaseModel(models.Model):
    class Meta:
        database = db


class Faculty(BaseModel):
    name = models.CharField(max_length=255)
    students_count = models.IntegerField()
    teacher_to_student_ratio = models.IntegerField()
    local_fulltime_specialist_count = models.IntegerField()
    foreign_fulltime_specialist_count = models.IntegerField()
    local_fulltime_supportive_count = models.IntegerField()
    foreign_fulltime_supportive_count = models.IntegerField()
    parttime_specialist_count = models.IntegerField()
    parttime_supportive_count = models.IntegerField()
    master_count = models.IntegerField()


class Tax(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class TaxLayer(BaseModel):
    from_ = models.IntegerField()
    to_ = models.IntegerField()
    rate = models.FloatField()
    tax = models.ForeignKeyField(Tax, backref="layers")


class Setting(BaseModel):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


db.create_tables([Faculty, Tax, TaxLayer, Setting])

if Setting.select().count() == 0:
    Setting.create(key="social_security_deduction_rate", value=0.07)
    Setting.create(key="social_security_minimum_salary", value=279000)
    Setting.create(key="locality_percentage", value=0.5)
    Setting.create(key="compensation_tax_rate", value=0.05)

if Tax.select().count() == 0:
    Tax.create(name="Syrian Layers Tax", description="Default taxes")
    TaxLayer.create(from_=0, to_=279_000, rate=0, tax_id=1)
    TaxLayer.create(from_=279_001, to_=450_000, rate=0.07, tax_id=1)
    TaxLayer.create(from_=450_001, to_=650_000, rate=0.09, tax_id=1)
    TaxLayer.create(from_=650_001, to_=850_000, rate=0.11, tax_id=1)
    TaxLayer.create(from_=850_001, to_=1_100_000, rate=0.13, tax_id=1)
    TaxLayer.create(from_=1_100_001, to_=50_000_000, rate=0.15, tax_id=1)
