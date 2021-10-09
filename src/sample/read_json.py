import sys
from paeon.json_timeline import JsonTimeline


SETTINGS = dict(
    part_number_prefix='Part',
    chapter_number_prefix='Chapter',
    part_desc_label='Label',
    chapter_desc_label='Label',
    scene_desc_label='Summary',
    scene_title_label='Label',
    notes_label='Notes',
    tag_label='Tags',
    location_label='Location',
    item_label='Item',
    character_label='Participant',
    viewpoint_label='Viewpoint',
)


kwargs = {'suffix': ''}
kwargs.update(SETTINGS)

timeline = JsonTimeline(sys.argv[1], **kwargs)
print(timeline.read())
