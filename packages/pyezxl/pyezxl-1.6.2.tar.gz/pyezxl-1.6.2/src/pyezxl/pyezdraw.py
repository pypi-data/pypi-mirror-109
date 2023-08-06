class pyezdraw:
	def __init__(self):
		self.test = "test"

	def draw_sheet_line(self, **input):
		#기본자료이다
		enum_line = {
		"msoArrowheadNone" : 1, "msoArrowheadTriangle" : 2,	"msoArrowheadOpen" : 3,	"msoArrowheadStealth" : 4,	"msoArrowheadDiamond" : 5,	"msoArrowheadOval" : 6,
		"" : 1, "<" : 2, ">o" : 3, ">>" : 4, ">" : 2, "<>" : 5, "o" : 6,
		"basic" : 1,	"none" : 1,	"triangle" : 2,	"open" : 3,	"stealth" : 4,	"diamond" : 5,	"oval" : 6,
		"msoArrowheadNarrow" : 1, "msoArrowheadWidthMedium" : 2, "msoArrowheadWide" : 3,
		"msoArrowheadShort" : 1, "msoArrowheadLengthMedium" : 2, "msoArrowheadLong" : 3,
		"short" : 1, "narrow" : 1, "medium" : 2,"long" : 3, "wide" : 3,
		"-1" : 1,  "0" : 2, "+1" : 3,
		"dash": 4, "dashdot": 5, "dashdotdot": 6, "rounddot": 3, "longdash": 7, "longdashdot": 8, "longdashdotdot": 9, "squaredot": 2,
		"-": 4, "-.": 5, "-..": 6, ".": 3, "--": 7, "--.": 8, "--..": 9,"ㅁ": 2,
		}

		base_data = {
			"sheet_name" : "",
			"xyxy" : [100,100,0,0],
			"color" :"pink++",
			"line_style" :"-.",
			"thickness":0.5,
			"transparency":0,
			"line_length" :400,
			"head_style" : ">",
			"head_length" : "0",
			"head_width" : "0",
			"tail_style" : ">",
			"tail_length" : "0",
			"tail_width" : "0",
		}

		#기본자료에 입력받은값을 update하는것이다
		base_data.update(input)

		#set_line.Select()
		sheet = self.check_sheet_name(enum_line[base_data["sheet_name"]])
		set_line = sheet.Shapes.AddLine(enum_line[base_data["xyxy"]])
		set_line.Line.ForeColor.RGB = enum_line[base_data["color"]]
		set_line.Line.DashStyle = enum_line[base_data["line_style"]]
		set_line.Line.Weight = enum_line[base_data["thickness"]]
		set_line.Line.Width = enum_line[base_data["line_length"]]
		set_line.Line.Transparency = enum_line[base_data["transparency"]] #투명도

		set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
		set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
		set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
		set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]] #화살표의 머리의 모양
		set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]] #화살표의 길이
		set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]] #화살표의 넓이


