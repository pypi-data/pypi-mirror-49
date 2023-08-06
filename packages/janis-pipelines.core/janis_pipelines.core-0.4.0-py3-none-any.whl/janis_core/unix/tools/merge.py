from janis_core import File, Array, ToolInput, ToolOutput, Stdout
from janis_core.unix.tools.unixtool import UnixTool


class Merge(UnixTool):
    def friendly_name(self) -> str:
        return "Merge Files"

    @staticmethod
    def tool():
        return "merge"

    @staticmethod
    def base_command():
        return ["cat"]

    def inputs(self):
        return [ToolInput("files", Array(File()))]

    def outputs(self):
        return [ToolOutput("out", Stdout())]
