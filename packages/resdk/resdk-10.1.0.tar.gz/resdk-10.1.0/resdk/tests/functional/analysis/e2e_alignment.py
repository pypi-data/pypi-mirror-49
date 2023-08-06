# pylint: disable=missing-docstring
from resdk.tests.functional.base import BaseResdkFunctionalTest


class TestAligners(BaseResdkFunctionalTest):

    def test_bowtie2(self):
        collection = self.res.collection.create(name='Test collection')

        # pylint: disable=unbalanced-tuple-unpacking
        reads_1, reads_2 = self.get_reads(2, collection)
        # pylint: enable=unbalanced-tuple-unpacking
        reads_3 = self.get_reads(1)[0]
        genome = self.get_genome()

        group = collection.create_group_relation(category='test', samples=[reads_1.sample])

        # Run bowtie on a collection
        bams = collection.run_bowtie2(genome=genome)
        self.assertEqual(len(bams), 2)
        self.assertEqual(bams[0].input['reads'], reads_1.id)
        self.assertEqual(bams[0].input['genome'], genome.id)
        self.assertEqual(bams[1].input['reads'], reads_2.id)
        self.assertEqual(bams[1].input['genome'], genome.id)

        # Run bowtie on a relation
        bams = group.run_bowtie2(genome=genome)
        self.assertEqual(len(bams), 1)
        self.assertEqual(bams[0].input['reads'], reads_1.id)
        self.assertEqual(bams[0].input['genome'], genome.id)

        # Run bowtie on a sample
        bams = reads_3.sample.run_bowtie2(genome=genome)
        self.assertEqual(len(bams), 1)
        self.assertEqual(bams[0].input['reads'], reads_3.id)
        self.assertEqual(bams[0].input['genome'], genome.id)

        # Run bowtie on a reads data object
        bams = reads_3.run_bowtie2(genome=genome)
        self.assertEqual(bams.input['reads'], reads_3.id)
        self.assertEqual(bams.input['genome'], genome.id)

    def test_hisat2(self):
        collection = self.res.collection.create(name='Test collection')

        # pylint: disable=unbalanced-tuple-unpacking
        reads_1, reads_2 = self.get_reads(2, collection)
        # pylint: enable=unbalanced-tuple-unpacking
        reads_3 = self.get_reads(1)[0]
        genome = self.get_genome()

        group = collection.create_group_relation(category='test', samples=[reads_1.sample])

        # Run hisat on a collection
        bams = collection.run_hisat2(genome=genome)
        self.assertEqual(len(bams), 2)
        self.assertEqual(bams[0].input['reads'], reads_1.id)
        self.assertEqual(bams[0].input['genome'], genome.id)
        self.assertEqual(bams[1].input['reads'], reads_2.id)
        self.assertEqual(bams[1].input['genome'], genome.id)

        # Run hisat on a relation
        bams = group.run_hisat2(genome=genome)
        self.assertEqual(len(bams), 1)
        self.assertEqual(bams[0].input['reads'], reads_1.id)
        self.assertEqual(bams[0].input['genome'], genome.id)

        # Run hisat on a sample
        bams = reads_3.sample.run_hisat2(genome=genome)
        self.assertEqual(len(bams), 1)
        self.assertEqual(bams[0].input['reads'], reads_3.id)
        self.assertEqual(bams[0].input['genome'], genome.id)

        # Run hisat on a reads data object
        bams = reads_3.run_hisat2(genome=genome)
        self.assertEqual(bams.input['reads'], reads_3.id)
        self.assertEqual(bams.input['genome'], genome.id)
