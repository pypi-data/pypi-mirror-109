
from ulab_image_contrast.core.tools import cmd_contrast_any_with_report


def command_contrast(options, args):
    print(options.original)
    print(options.modified)
    cmd_contrast_any_with_report(options.original, options.modified,report_dir=options.report_dir,combine_marked_image = options.combine_marked_image)
    #ssim(options.original, options.modified)
