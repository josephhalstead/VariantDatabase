from django.contrib import admin
from .models import *

admin.site.register(Section)
admin.site.register(SubSection)
admin.site.register(Worksheet)
admin.site.register(Sample)
admin.site.register(Variant)
admin.site.register(VariantSample)
admin.site.register(Gene)
admin.site.register(Consequence)
admin.site.register(Transcript)
admin.site.register(VariantTranscript)
admin.site.register(Report)
admin.site.register(ReportVariant)
admin.site.register(ReadLaneQuality)
admin.site.register(GeneCoverage)
admin.site.register(ExonCoverage)
admin.site.register(Comment)
admin.site.register(Evidence)
admin.site.register(UserSetting)