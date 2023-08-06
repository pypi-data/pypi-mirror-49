from janis_bioinformatics.tools import BioinformaticsWorkflow
from janis_core import Step, Input, Output, Array
from janis_bioinformatics.data_types import Vcf, VcfIdx
from janis_bioinformatics.tools.gatk4 import Gatk4GenotypeConcordanceLatest
from janis_bioinformatics.tools.htslib import BGZip_1_2_1, Tabix_1_2_1


class PerformanceValidator_1_2_1(BioinformaticsWorkflow):
    def __init__(self):
        super(PerformanceValidator_1_2_1, self).__init__(
            "performanceValidator", friendly_name="Performance Validator"
        )

        inp = Input("vcf", Vcf())
        inp_truth = Input("truth", VcfIdx())
        inp_intervals = Input("intervals", Array(Vcf()))

        s1_bgzip = Step("s1_bgzip", BGZip_1_2_1())
        s2_tabix = Step("s2_tabix", Tabix_1_2_1())
        s3_genotypeconcord = Step(
            "s3_genotypeconcord", Gatk4GenotypeConcordanceLatest()
        )

        self.add_edges(
            [
                (inp, s1_bgzip.file),
                (s1_bgzip.out, s2_tabix.file),
                (s2_tabix.out, s3_genotypeconcord.callVCF),
                (inp_truth, s3_genotypeconcord.truthVCF),
                (inp_intervals, s3_genotypeconcord.intervals),
            ]
        )

        self.add_default_value(s3_genotypeconcord.treatMissingSitesAsHomeRef, True)

        self.add_edges(
            [
                (s3_genotypeconcord.summaryMetrics, Output("summaryMetrics")),
                (s3_genotypeconcord.detailMetrics, Output("detailMetrics")),
                (s3_genotypeconcord.contingencyMetrics, Output("contingencyMetrics")),
            ]
        )


if __name__ == "__main__":
    print(PerformanceValidator_1_2_1().help())
