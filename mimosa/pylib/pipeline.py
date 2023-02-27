from plants.pylib.patterns import term_patterns as t_patterns
from plants.pylib.pipeline_builder import PipelineBuilder


def pipeline():
    pipe = PipelineBuilder()
    pipe.add_tokenizer_pipe()
    pipe.add_term_patterns(t_patterns.TERMS.terms, t_patterns.REPLACE)
    pipe.add_range_patterns()
    pipe.add_parts_patterns()
    pipe.add_simple_patterns()
    pipe.add_numeric_patterns()
    pipe.add_part_locations_patterns()
    pipe.add_taxa_patterns()
    pipe.add_taxon_plus_patterns()
    pipe.add_taxon_like_patterns()
    pipe.add_color_patterns()
    pipe.add_group_traits_patterns()
    pipe.add_delete_partial_traits_patterns()
    pipe.add_merge_pipe()
    pipe.add_link_parts_patterns()
    pipe.add_link_parts_once_patterns()
    pipe.add_link_subparts_patterns()
    pipe.add_link_subparts_suffixes_patterns()
    pipe.add_link_sex_patterns()
    pipe.add_link_location_patterns()
    pipe.add_link_taxa_like_patterns()
    pipe.add_delete_unlinked_patterns()
    return pipe
