from iso import Iso, C


def cover_stack():
    s = Iso(S=9, ox=250, oy=215, w=600, h=445)
    layers = [("esg", "ESG · esgOS", 0), ("data", "DATA · ergOS", 1), ("heat", "HEAT · HEAT PUMPS", 2), ("green", "POWER · GREEN SUPPLY", 3)]
    # draw bottom (power) first
    for key, label, i in reversed(layers):
        z = (3 - i) * 7
        col = C[key]
        s.box(0, 0, z, 22, 22, 1.1, col, top="#101a15" if key == "green" else "#121518", sw=1.3)
        for k in range(1, 5):
            s.line([(22 * k / 5, 0, z + 1.1), (22 * k / 5, 22, z + 1.1)], col, .45, op=.35)
            s.line([(0, 22 * k / 5, z + 1.1), (22, 22 * k / 5, z + 1.1)], col, .45, op=.35)
        X, Y = s.xy(22, 11, z + .5)
        s.out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" stroke-dasharray="2 3"/>' % (X, Y, 470, Y - 30, col))
        s.out.append('<text x="478" y="%.1f" fill="%s" font-size="13" letter-spacing="2" font-family="IBM Plex Mono, monospace" dominant-baseline="central">%s</text>' % (Y - 30, col, label.split(" · ")[0]))
        s.out.append('<text x="478" y="%.1f" fill="#8b949a" font-size="11" letter-spacing="1.2" font-family="IBM Plex Mono, monospace" dominant-baseline="central">%s</text>' % (Y - 13, label.split(" · ")[1]))
    # vertical energy risers through the stack
    for (x, y) in [(6, 6), (16, 6), (11, 16)]:
        s.flow([(x, y, 1.1), (x, y, 22.1)], C["green"], 1.6)
    return s.render("The jouleWise decarbonisation stack: power, heat, data and ESG layers")


def automotive():
    s = Iso(S=7.6, ox=345, oy=178, w=800, h=585)
    s.ground(-3, 8, 58, 44)
    # ---- off-site green supply
    s.solarfield(0, -15, 15, rows=4)
    s.turbine(22, -13, 17, 10)
    s.turbine(28, -15, 17, 70)
    s.turbine(33, -12, 15, 40)
    p1 = s.pylon(36, -8, 10)
    p2 = s.pylon(40, -3.5, 10)
    s.line([p1, p2, (44, 2, 3)], "#5d676e", .8)
    # ---- substation + BESS
    s.box(40, 0, 0, 9, 7, .4)
    s.box(41, 1, .4, 2.6, 2.2, 2.6, C["green"])
    s.box(45, 1, .4, 2.6, 2.2, 2.6, C["green"])
    s.box(41, 4.3, .4, 6.6, 1.6, 1.4)
    s.container(51, -.5, 0, 6.5, 2.4, 2.6, C["green"])
    s.container(51, 2.7, 0, 6.5, 2.4, 2.6, C["green"])
    # ---- power bus on the ground
    s.flow_now([(44, 7, .1), (44, 8.6, .1), (-1, 8.6, .1)], C["green"], 1.6)
    s.flow([(44, 8.6, .1), (46.5, 8.6, .1), (46.5, 11, .1)], C["green"], 1.6)
    # ---- process row
    s.box(0, 11, 0, 14, 13, 6)
    s.windows(0, 11, 0, 14, 13, 6, 5, "left")
    s.panels(.8, 11.8, 6, 12.4, 11.4, rows=4)
    s.sawtooth(16, 11, 0, 12, 13, 5.5, 4)
    s.windows(16, 11, 0, 12, 13, 5.5, 4, "left")
    s.cyl(29, 12, 0, .8, 17)
    s.rings(29, 12, 0, .8, [6, 12], "#4a535a")
    s.cut_open(30, 11, 0, 12, 13, 8)
    s.box(30.6, 11.5, 0, 10.8, 3.2, 4, top="#23282c")
    for i in range(6):
        s.box(31.2 + i * 1.8, 11.5, 1, .9, .05, 2, top="#f2994a", left="#6b3a1a", right="#6b3a1a")
    s.line([(30.5, 18.3, 5), (41.5, 18.3, 5)], "#8a949b", 1.4)
    for i in range(3):
        tx = 31 + i * 3.6
        s.box(tx, 16.6, 0, 3.1, 3.4, 1.3, C["heat"], top="#1d4266", sw=1.1)
        s.line([(tx + 1.6, 18.3, 5), (tx + 1.6, 18.3, 2.6)], "#8a949b", .8)
        s.car(tx - .25, 17.5, 1.1 if i == 1 else 1.7, col=["#2c4a66", "#3a5f80", "#6b7b88"][i])
    s.person(38, 22.2)
    s.cut_close(30, 11, 0, 12, 13, 8, 1.1)
    s.hp(45, 11.5, 0, 4, 3)
    s.hp(45, 16, 0, 4, 3)
    s.flow([(45, 13, 1.2), (42, 13, 1.2)], C["heat"], 1.8)
    s.flow([(45, 17.5, 1.2), (41, 18, 1.2), (34, 18, 1.2)], C["heat"], 1.8)
    s.cyl(47, 23.5, 0, 1.7, 6, C["heat"], fill="#1f160d", sw=1.2)
    s.rings(47, 23.5, 0, 1.7, [2, 4], "#6b4a2a")
    s.flow([(47, 21.8, 1), (47, 19, 1)], C["heat"], 1.6)
    # ---- inbound steel coils
    s.truck(-1, 26.3, 7, cargo="#3a4147")
    for i in range(3):
        s.cyl(.4 + i * 2.1, 27.4, 3.2, .75, .9, fill="#4a535a", topfill="#5d676e")
    # ---- front row
    s.box(2, 32, 0, 6, 4, 3, C["data"], left="#101a2a")
    s.windows(2, 32, 0, 6, 4, 3, 3, "left", "#2a4a7a")
    s.shed(12, 30, 0, 20, 9, 5, 2.2)
    s.windows(12, 30, 0, 20, 9, 5, 6, "left")
    s.box(36, 30, 0, 6, 4.5, 3, C["heat"])
    s.windows(36, 30, 0, 6, 4.5, 3, 3, "left", "#3a2a18")
    s.flow([(42, 32, .8), (47, 32, .8), (47, 25.2, .8)], C["heat"], 1.6)
    s.person(10, 38.5)
    s.person(34, 37)
    s.person(49, 29, hat="#ffffff")
    s.carcarrier(44, 37, None)
    s.carcarrier(39, 42.5, None)
    # ---- markers
    s.mark(1, (7, -11, 1), "power", 0, -40)
    s.mark(2, (44, 2, 3), "power", -30, -56)
    s.mark(3, (7, 17, 6.6), "power", 24, -62)
    s.mark(4, (54, 1, 2.6), "power", 26, -40)
    s.mark(5, (47, 13, 2.7), "heat", 50, -30)
    s.mark(6, (47, 23.5, 6), "heat", 62, 18)
    s.mark(7, (39, 31, 3), "heat", 0, -50)
    s.mark(8, (5, 33, 3), "data", -38, 34)
    s.mark(9, (2, 27, 3.2), "esg", -34, -52)
    s.mark(10, (49, 38, 2), "esg", 44, 10)
    return s.render("Automotive plant supply chain with jouleWise intervention points")


def backdrop(s):
    """shared off-site green supply, substation, BESS and power bus (markers 1, 2, 4)"""
    s.ground(-3, 8, 58, 44)
    s.solarfield(0, -15, 15, rows=4)
    s.turbine(22, -13, 17, 10)
    s.turbine(28, -15, 17, 70)
    s.turbine(33, -12, 15, 40)
    p1 = s.pylon(36, -8, 10)
    p2 = s.pylon(40, -3.5, 10)
    s.line([p1, p2, (44, 2, 3)], "#5d676e", .8)
    s.box(40, 0, 0, 9, 7, .4)
    s.box(41, 1, .4, 2.6, 2.2, 2.6, C["green"])
    s.box(45, 1, .4, 2.6, 2.2, 2.6, C["green"])
    s.box(41, 4.3, .4, 6.6, 1.6, 1.4)
    s.container(51, -.5, 0, 6.5, 2.4, 2.6, C["green"])
    s.container(51, 2.7, 0, 6.5, 2.4, 2.6, C["green"])
    s.flow_now([(44, 7, .1), (44, 8.6, .1), (-1, 8.6, .1)], C["green"], 1.6)
    s.flow_now([(44, 8.6, .1), (46.5, 8.6, .1), (46.5, 11, .1)], C["green"], 1.6)
    s.mark(1, (7, -11, 1), "power", 0, -40)
    s.mark(2, (44, 2, 3), "power", -30, -56)
    s.mark(4, (54, 1, 2.6), "power", 26, -40)


def pharma():
    s = Iso(S=7.6, ox=345, oy=178, w=800, h=585)
    backdrop(s)
    STEEL = "#2a3036"
    # API block
    s.box(0, 11, 0, 12, 13, 11)
    s.windows(0, 11, 0, 12, 13, 5.5, 4, "left")
    s.windows(0, 11, 5.5, 12, 13, 5.5, 4, "left")
    s.windows(0, 11, 0, 12, 13, 11, 4, "right")
    s.box(2, 13, 11, 3, 3, 1.4)
    s.cyl(8, 15, 11, .6, 3)
    # reactor bay
    s.box(14, 11, 0, 11, 8, .6)
    for x in (16.2, 19.6, 23):
        s.cyl(x, 14.5, .6, 1.35, 5.8, fill=STEEL, topfill="#3a4147")
        s.rings(x, 14.5, .6, 1.35, [1.5, 3.2], C["heat"])
        s.cyl(x, 14.5, 6.4, .35, 1.2, fill=STEEL)
    # dryer
    s.box(14, 21, 0, 10, 5, 4)
    s.windows(14, 21, 0, 10, 5, 4, 3, "left")
    s.cyl(22.5, 22.5, 4, .6, 3)
    # cleanroom formulation block with AHUs on roof
    s.box(27, 11, 0, 16, 6, 6.5)
    for i, x in enumerate((28, 32.8, 37.6)):
        acc = C["heat"] if i >= 1 else None
        s.box(x, 12, 6.5, 4, 3.4, 1.5, acc)
        s.ellipse_top(x + 2, 13.7, 8, .8, acc or C["stroke"], "#141719")
    s.cut_open(27, 17, 0, 16, 9, 6.5)
    s.box(27.4, 17.3, 5.2, 15.2, .8, .7, top="#2a3036")
    for k in range(3):
        s.line([(31 + k * 4.5, 17.4, 5.2), (31 + k * 4.5, 17.4, 4.4)], "#8a949b", .8)
    s.box(28.2, 18.6, 0, 2.6, 2.2, 2, C["data"], top="#1b2a44")
    s.cyl(29.5, 19.7, 2, .5, .6, fill="#2a3036")
    s.box(30.8, 19.2, 0, 11, 1, .8, top="#2f363c")
    for k in range(13):
        s.cyl(31.3 + k * .8, 19.7, .8, .17, .45, fill="#3a4a58", topfill="#c9d6e0", sw=.4)
    s.line([(28, 22.2, 0), (42, 22.2, 0), (42, 22.2, 4), (28, 22.2, 4), (28, 22.2, 0)], "#5b8def", .7, op=.6)
    s.box(33, 23.2, 0, 3, 2, 1.6, top="#2f363c")
    s.cyl(34.5, 24.2, 1.6, .5, .8, fill="#2a3036")
    s.person(38.5, 21, hat="#ffffff")
    s.person(31.5, 25, hat="#ffffff")
    s.cut_close(27, 17, 0, 16, 9, 6.5, 1.0)
    # utility yard: heat pumps, cooling tower, PW/WFI tanks, hot water store
    s.hp(45, 11.5, 0, 4, 3)
    s.hp(45, 16, 0, 4, 3)
    s.flow([(45, 13, 1.2), (43.5, 13, 1.2), (43.5, 13, 7.2), (41.6, 13.5, 7.2)], C["heat"], 1.8)
    s.cyl(54, 13.5, 0, 1.9, 4.2, fill="#141a1c")
    s.ellipse_top(54, 13.5, 4.2, 1.2, "#6b757c", "#0c0e10")
    s.flow([(52.2, 13.5, 1.2), (49, 13.2, 1.2)], C["heat"], 1.6)
    for x in (47, 50.4):
        s.cyl(x, 23, 0, 1.25, 5, fill="#20262b", topfill="#39414a")
    s.cyl(54.2, 23, 0, 1.7, 6, C["heat"], fill="#1f160d", sw=1.2)
    s.rings(54.2, 23, 0, 1.7, [2, 4], "#6b4a2a")
    s.flow([(54.2, 21.3, 1), (48, 19, 1)], C["heat"], 1.6)
    # inbound KSM drums
    s.truck(-1, 26.3, 7, cargo="#3a4147")
    for i in range(4):
        s.cyl(.3 + i * 1.6, 27.4, 3.2, .6, 1.1, fill="#2a4a3a", topfill="#3a6a52")
    # front row
    s.box(2, 32, 0, 6, 4, 3, C["data"], left="#101a2a")
    s.windows(2, 32, 0, 6, 4, 3, 3, "left", "#2a4a7a")
    s.box(12, 30, 0, 22, 10, 6)
    s.windows(12, 30, 0, 22, 10, 6, 7, "left")
    s.panels(12.8, 30.8, 6, 20.4, 8.4, rows=3)
    s.box(36, 31, 0, 5, 4, 3)
    s.person(10, 38.5)
    s.person(35, 38)
    s.person(51, 29, hat="#ffffff")
    for (x, y) in ((42, 36.5), (37, 42)):
        s.truck(x, y, 7, cargo="#1d3550")
        s.box(x, y, 3.2, 1, 2.2, .7, C["data"])
    # markers
    s.mark(3, (23, 35, 6.6), "power", 0, -62)
    s.mark(5, (47, 13, 2.7), "heat", 50, -30)
    s.mark(6, (39.6, 13.7, 8), "heat", -30, -62)
    s.mark(7, (54.2, 23, 6), "heat", 30, 56)
    s.mark(8, (54, 13.5, 4.2), "heat", 66, 22)
    s.mark(9, (5, 33, 3), "data", -38, 34)
    s.mark(10, (2, 27, 4.3), "esg", -34, -52)
    return s.render("Pharmaceutical plant supply chain with jouleWise intervention points")


def textile():
    s = Iso(S=7.6, ox=345, oy=178, w=800, h=585)
    backdrop(s)
    # spinning mill with rooftop solar
    s.box(0, 11, 0, 12, 13, 6)
    s.windows(0, 11, 0, 12, 13, 6, 4, "left")
    s.panels(.8, 11.8, 6, 10.4, 11.4, rows=4)
    # weaving shed
    s.sawtooth(14, 11, 0, 12, 13, 5, 4)
    s.windows(14, 11, 0, 12, 13, 5, 4, "left")
    # dye house with existing boiler stack
    s.cyl(27, 12, 0, .8, 16)
    s.rings(27, 12, 0, .8, [6, 11], "#4a535a")
    s.cut_open(28, 11, 0, 13, 13, 7)
    s.box(28.4, 11.4, 5.4, 12.2, .6, .6, top="#2a3036")
    for x in (30.2, 33.4, 36.6):
        s.cyl(x, 13.4, 0, 1.15, 3.2, fill="#2a3036", topfill="#3a4147")
        s.rings(x, 13.4, 0, 1.15, [1, 2.2], C["heat"])
        s.cyl(x, 13.4, 3.2, .35, .5, fill="#2a3036")
    for x in (29.2, 34.6):
        s.box(x, 17, 0, 4.4, 2.4, 1.9, top="#2f363c")
        s.ellipse_top(x + 1.1, 18.2, 1.9, .5, C["heat"], "#2a1d10")
        s.line([(x + 4.4, 18.2, 1.4), (x + 4.9, 18.2, 2.6)], "#b14a6a", 2.2)
    for x, col in ((29.5, "#b14a6a"), (32.4, "#3a6ab1"), (35.3, "#c9a43a"), (38.2, "#2f8f6a")):
        s.box(x, 21.3, 0, 2, 1.5, .3, top="#3a4147")
        s.box(x + .1, 21.4, .3, 1.8, 1.3, 1.1, top=col, left="#20262b", right="#1a1f23")
    s.person(33.8, 20.6)
    s.cut_close(28, 11, 0, 13, 13, 7, 1.0)
    # heat pumps + hot water store
    s.hp(45, 11.5, 0, 4, 3)
    s.hp(45, 16, 0, 4, 3)
    s.flow([(45, 13, 1.2), (41, 13, 1.2)], C["heat"], 1.8)
    s.flow([(45, 17.5, 1.2), (39, 18.2, 1.2)], C["heat"], 1.8)
    s.cyl(47, 23.5, 0, 1.8, 6.5, C["heat"], fill="#1f160d", sw=1.2)
    s.rings(47, 23.5, 0, 1.8, [2, 4.2], "#6b4a2a")
    s.flow([(47, 21.7, 1), (47, 19, 1)], C["heat"], 1.6)
    # inbound bales
    s.truck(-1, 26.3, 7, cargo="#3a4147")
    for i in range(3):
        s.box(0 + i * 2.1, 26.6, 3.2, 1.8, 1.6, 1.2, top="#d8d4c8", left="#a9a598", right="#8e8a7e")
    # control room
    s.box(2, 32, 0, 6, 4, 3, C["data"], left="#101a2a")
    s.windows(2, 32, 0, 6, 4, 3, 3, "left", "#2a4a7a")
    # stenter line with exhaust heat recovery
    s.box(12, 31, 0, 22, 5, 3.4)
    s.windows(12, 31, 0, 22, 5, 3.4, 8, "left")
    for x in (15, 20, 25):
        s.cyl(x, 33, 3.4, .45, 2.2)
    s.box(28.5, 31.8, 3.4, 4, 3, 1.4, C["heat"])
    s.flow([(30.5, 33.3, 4.8), (30.5, 33.3, 6), (43, 33.3, 6), (43, 25, 6), (45.5, 23.5, 6)], C["heat"], 1.4)
    # ETP basins + equalisation tank (warm effluent)
    for (x, y) in ((44, 30), (50, 30), (44, 36)):
        s.box(x, y, 0, 5, 5, .9, top="#16324c")
        s.poly([(x + .4, y + .4, .9), (x + 4.6, y + .4, .9), (x + 4.6, y + 4.6, .9), (x + .4, y + 4.6, .9)], "#1d4266", "#2d5a86", .6)
    s.cyl(53, 38.5, 0, 1.6, 3.2, C["heat"], fill="#141a1c", sw=1.1)
    s.flow([(51.5, 37.5, 1), (56.5, 34, 1), (56.5, 27, 1), (50, 17, 1)], C["heat"], 1.6)
    # outbound export container
    s.truck(30, 40.5, 8, cargo="#2a3b4a")
    s.person(10, 38.5)
    s.person(38, 29.5)
    s.person(42, 38, hat="#ffffff")
    # markers
    s.mark(3, (6, 17, 6.6), "power", 24, -62)
    s.mark(5, (47, 13, 2.7), "heat", 50, -30)
    s.mark(6, (53, 38.5, 3.2), "heat", 56, 20)
    s.mark(7, (47, 23.5, 6.5), "heat", 62, 46)
    s.mark(8, (30.5, 33.3, 4.8), "heat", 0, -56)
    s.mark(9, (5, 33, 3), "data", -38, 34)
    s.mark(10, (34, 41.5, 3.2), "esg", -46, 26)
    return s.render("Textile mill supply chain with jouleWise intervention points")


def hotel():
    s = Iso(S=7.6, ox=345, oy=178, w=800, h=585)
    backdrop(s)
    # podium with rooftop solar, pool
    s.box(3, 11, 0, 27, 17, 4)
    s.windows(3, 11, 0, 27, 17, 4, 8, "left", "#2b3a44")
    s.windows(3, 11, 0, 27, 17, 4, 5, "right", "#2b3a44")
    s.panels(3.8, 11.8, 4, 9, 15.4, rows=5)
    s.poly([(24.5, 22.5, 4.02), (29.2, 22.5, 4.02), (29.2, 27.2, 4.02), (24.5, 27.2, 4.02)], "#1d4a6e", C["heat"], 1.2)
    s.poly([(25.2, 23.2, 4.05), (28.5, 23.2, 4.05), (28.5, 26.5, 4.05), (25.2, 26.5, 4.05)], "#2a6a96", "#3f86b8", .6)
    # tower
    s.box(14, 13, 4, 9, 8, 15)
    for k in range(5):
        s.windows(14, 13, 4 + k * 3, 9, 8, 3, 4, "left", "#2e3a44")
        s.windows(14, 13, 4 + k * 3, 9, 8, 3, 3, "right", "#2e3a44")
    s.box(16, 15, 19, 4, 4, 1.4)
    # laundry block with existing boiler stack
    s.cyl(31.1, 12, 0, .6, 10)
    s.cut_open(32, 11, 0, 9, 9, 5)
    for i in range(3):
        x = 32.6 + i * 2.7
        s.box(x, 11.6, 0, 2.2, 2, 2.3, top="#3a4147", left="#2a3036", right="#20262b")
        s.disc_y(x + 1.1, 13.62, 1.2, .7, "#16324c", C["heat"])
    s.box(32.8, 15.2, 0, 6.6, 1.6, 1.1, top="#2f363c")
    for k in range(4):
        s.line([(33.3 + k * 1.6, 15.2, 1.1), (33.3 + k * 1.6, 16.8, 1.1)], "#8a949b", 1.1)
    for x in (33.2, 36.4):
        s.box(x, 17.8, 0, 2, 1.4, 1.2, top="#e6e2d6", left="#b9b5a8", right="#9d998d")
    s.person(39.6, 18.6)
    s.cut_close(32, 11, 0, 9, 9, 5, .9)
    # chillers
    for x in (32.5, 36.8):
        s.box(x, 22.5, 0, 3.6, 4.5, 2.4)
        s.ellipse_top(x + 1.8, 23.8, 2.4, .7, C["stroke"], "#141719")
        s.ellipse_top(x + 1.8, 25.8, 2.4, .7, C["stroke"], "#141719")
    # heat pumps + store
    s.hp(45, 11.5, 0, 4, 3)
    s.hp(45, 16, 0, 4, 3)
    s.flow([(45, 13, 1.2), (41, 13, 1.2)], C["heat"], 1.8)
    s.flow([(40.4, 24.5, 1.2), (44, 24.5, 1.2), (46, 19, 1.2)], C["heat"], 1.6)
    s.cyl(47.5, 24, 0, 1.7, 6, C["heat"], fill="#1f160d", sw=1.2)
    s.rings(47.5, 24, 0, 1.7, [2, 4], "#6b4a2a")
    s.flow([(45, 17.5, 1.2), (30, 17.5, 1.2), (30, 22, 4)], C["heat"], 1.4)
    # control room
    s.box(2, 32, 0, 6, 4, 3, C["data"], left="#101a2a")
    s.windows(2, 32, 0, 6, 4, 3, 3, "left", "#2a4a7a")
    # arrival canopy, cars, EV chargers
    s.box(11, 30, 3, 13, 5, .4)
    for (x, y) in ((11.3, 34.4), (23.4, 34.4)):
        s.box(x, y, 0, .3, .3, 3)
    for i, x in enumerate((13, 17.5)):
        s.box(x, 31, .3, 3.4, 1.8, 1, top="#2a3b4a")
        s.box(x + .6, 31.2, 1.3, 2, 1.4, .6, top="#35495b")
    for x in (28, 31, 34):
        s.box(x, 32, 0, .6, .6, 1.8, C["green"])
        s.box(x - .6, 33.4, .3, 2.4, 1.6, .9, top="#2a3b4a")
    s.person(20, 37)
    s.person(9, 37, hat="#ffffff")
    s.person(38, 29)
    # linen van
    s.truck(40, 38, 6, cargo="#3a4147")
    # markers
    s.mark(3, (8, 19, 4.6), "power", -20, -60)
    s.mark(5, (47, 13, 2.7), "heat", 50, -30)
    s.mark(6, (35.4, 12.6, 2.3), "heat", -6, -86)
    s.mark(7, (27, 25, 4.1), "heat", -30, 95)
    s.mark(8, (35, 24.5, 2.4), "heat", 60, 60)
    s.mark(9, (5, 33, 3), "data", -38, 34)
    s.mark(10, (17, 32, 3.4), "esg", -30, 60)
    s.mark(11, (31, 32, 1.8), "power", 60, 70)
    return s.render("Hotel property with jouleWise intervention points")


def beverages():
    s = Iso(S=7.6, ox=345, oy=178, w=800, h=585)
    backdrop(s)
    # water treatment: silos + RO
    for x in (1.6, 5, 8.4):
        s.cyl(x, 13.2, 0, 1.4, 7, fill="#1a2228", topfill="#2a3640")
        s.rings(x, 13.2, 0, 1.4, [2.3, 4.6], "#3a4a56")
    s.box(0, 17.5, 0, 10.5, 7, 3)
    s.windows(0, 17.5, 0, 10.5, 7, 3, 4, "left", "#2a4a7a")
    # syrup room
    s.box(13, 11, 0, 12, 14, 7)
    s.windows(13, 11, 0, 12, 14, 7, 4, "left")
    for x in (15, 18.5, 22):
        s.cyl(x, 13.5, 7, 1.1, 2.2, fill="#2a3036", topfill="#3a4147")
    # bottling hall with rooftop solar
    s.cut_open(27, 11, 0, 16, 14, 6)
    s.box(27.4, 11.4, 4.8, 15.2, .6, .6, top="#2a3036")
    s.cyl(29.4, 14.6, 0, 1.5, 1.9, C["data"], fill="#1b2a44", topfill="#23385a")
    s.cyl(29.4, 14.6, 1.9, .5, 1.4, fill="#2a3036")
    s.box(31, 14.1, 0, 11, 1, .8, top="#2f363c")
    for k in range(13):
        s.bottle(31.5 + k * .82, 14.6, .8)
    s.box(28.5, 19.2, 0, 13.5, 1, .8, top="#2f363c")
    for k in range(16):
        s.bottle(29 + k * .82, 19.7, .8)
    s.box(38.4, 21.6, 0, 3.8, 2.4, 1.7, top="#2f363c")
    s.box(28.4, 21.8, 0, 3.2, 2.6, .25, top="#6b5a3a")
    for (a, b, c) in ((28.5, 21.9, .25), (30, 21.9, .25), (28.5, 23.1, .25), (30, 23.1, .25), (28.5, 21.9, 1.05), (30, 21.9, 1.05)):
        s.box(a, b, c, 1.4, 1.1, .8, top="#b14a3a", left="#7a3328", right="#5e271f")
    s.person(35.5, 17.2)
    s.person(36.5, 23.4)
    s.cut_close(27, 11, 0, 16, 14, 6, .95)
    # tunnel pasteuriser + bottle washer along the front
    s.box(27.5, 26, 0, 14, 2.4, 1.8, C["heat"], left="#23180c")
    for i in range(10):
        X, Y = s.xy(28.5 + i * 1.3, 26.6, 1.8)
        s.out.append('<rect x="%.1f" y="%.1f" width="2.4" height="4" rx=".8" fill="#3dd68c" opacity=".55"/>' % (X - 1.2, Y - 4))
    # heat pumps, CIP / hot water store, chillers
    s.hp(45, 11.5, 0, 4, 3)
    s.hp(45, 16, 0, 4, 3)
    s.box(51, 12, 0, 5, 6, 2.6)
    s.ellipse_top(52.5, 15, 2.6, .8, C["stroke"], "#141719")
    s.ellipse_top(54.5, 15, 2.6, .8, C["stroke"], "#141719")
    s.flow([(51, 15, 1.2), (49, 15, 1.2)], C["heat"], 1.6)
    s.flow([(45, 13, 1.2), (43, 13, 1.2)], C["heat"], 1.8)
    s.cyl(47, 23.5, 0, 1.6, 6, C["heat"], fill="#1f160d", sw=1.2)
    s.rings(47, 23.5, 0, 1.6, [2, 4], "#6b4a2a")
    s.cyl(51, 23.5, 0, 1.3, 5, fill="#20262b", topfill="#39414a")
    s.flow([(47, 21.9, 1), (47, 19, 1)], C["heat"], 1.6)
    s.flow([(45.4, 23.5, 1), (41.5, 27, 1)], C["heat"], 1.6)
    # inbound sugar / preforms
    s.truck(-1, 26.3, 7, cargo="#3a4147")
    for i in range(3):
        s.box(0 + i * 2.1, 26.6, 3.2, 1.8, 1.6, 1.1, top="#d8d4c8", left="#a9a598", right="#8e8a7e")
    # control room, warehouse, outbound
    s.box(2, 32, 0, 6, 4, 3, C["data"], left="#101a2a")
    s.windows(2, 32, 0, 6, 4, 3, 3, "left", "#2a4a7a")
    s.box(12, 31, 0, 22, 9, 5)
    s.windows(12, 31, 0, 22, 9, 5, 7, "left")
    s.panels(12.8, 31.8, 5, 20.4, 7.4, rows=3)
    for (x, y) in ((40, 34), (37, 40)):
        s.truck(x, y, 7, cargo="#2a3b4a")
        for k in range(3):
            s.box(x + .3 + k * 2.2, y + .2, 3.2, 2, 1.8, .9, top="#b14a3a", left="#7a3328", right="#5e271f")
    s.person(10, 38.5)
    s.person(36, 30)
    s.person(50, 29, hat="#ffffff")
    # markers
    s.mark(3, (23, 35, 5.6), "power", -10, -60)
    s.mark(5, (47, 13, 2.7), "heat", 50, -30)
    s.mark(6, (33, 27, 1.8), "heat", 64, 54)
    s.mark(7, (47, 23.5, 6), "heat", 62, 34)
    s.mark(8, (53.5, 15, 2.6), "heat", 64, -2)
    s.mark(9, (5, 33, 3), "data", -38, 34)
    s.mark(10, (44, 41, 4.1), "esg", 96, 40)
    s.mark(11, (5, 13.2, 7), "esg", -30, -52)
    return s.render("Beverage plant supply chain with jouleWise intervention points")
