from ..generation.rajat_work.qgen.generator.symsub import SymSubGenerator
from ..generation.rajat_work.qgen.generator.fpm.fpm import FPMGenerator
from ..generation.rajat_work.qgen.encoder.dummy import dummyEN
from ..generation.rajat_work.qgen.generator.eda import EDAGenerator
# from ..generation.broken_english.broken_english_generator import BrokenEnglishGen
from ..generation.sentAug.sentAug import AUG
from ..generation.t5_paraphrase_gen.t5_paraphrase import T5Generator
from .generation import GenerateManager

defaultNames = ["SymSub", "FPM", "EDA", "nlpAug", "T5"]
defaultNums = [3, 3, 3, 2, 3]

defaultGenerateManager = GenerateManager(
    producers=[SymSubGenerator(dummyEN("lite")), FPMGenerator(), EDAGenerator(), AUG(), T5Generator()],
    names=defaultNames,
    nums=defaultNums,
)
