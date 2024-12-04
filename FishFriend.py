import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.transforms as transforms
import matplotlib.colors as mcolors
import pandas as pd
import array as arr

from matplotlib.offsetbox import AnnotationBbox, TextArea, VPacker, HPacker, OffsetImage
from matplotlib.widgets import Slider
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib import patches

from CustomButtons import *

price_colors = ['black', 'gray', 'gold', 'darkviolet']

location_states = {
    'Forest Pond': False,
    'Ocean': False,
    'Forest River': False,
    'Town River': False,
    'Mountain Lake': False
    }

selected_price_type = 'Standard Price'
selected_season = 'Spring'

current_tooltip = None

fish_axes = []
fish_rectangle = None

pond_vertices = [(65, 107), (69, 107), (70, 108), (72, 108), (73, 109), (74, 109), (75, 110), (76, 110), (77, 111), (78, 112), 
                 (78, 116), (77, 117), (76, 118), (75, 119), (69, 119), (68, 118), (66, 118), (65, 117), (64, 117), (63, 116), 
                 (62, 115), (62, 114), (61, 114), (61, 111), (62, 109), (63, 109), (64, 108)]
pond_codes = [Path.MOVETO] + [Path.LINETO] * (len(pond_vertices) - 1) + [Path.CLOSEPOLY]
pond_path_vertices = pond_vertices + [pond_vertices[0]]
pond_path = Path(pond_path_vertices, pond_codes)
pond_patch = PathPatch(pond_path, facecolor = 'white', edgecolor = 'gray', alpha = 0.6)

ocean_vertices = [(0, 180), (0, 168), (1, 168), (2, 167), (3, 166), (7, 166), (7, 165), (10, 165), (10, 164), (12, 164), (12, 163), (15, 163), (15, 162), (17, 162), (17, 161),
                 (18, 161), (18, 160), (20, 160), (21, 159), (20, 159), (21, 158), (22, 158), (22, 157), (24, 157), (24, 156), (25, 156), (25, 155), (27, 155), (27, 154), 
                 (29, 154), (29, 153), (30, 153), (30, 152), (32, 152), (32, 151), (34, 151), (34, 149), (36, 149), (36, 147), (38, 145), (40, 144), (41, 143), (46, 143),
                 (48, 145), (48, 147), (49, 147), (49, 151), (50, 151), (50, 153), (52, 153), (52, 154), (56, 154), (56, 155), (64, 155), (64, 156), (67, 156), (67, 157),
                 (69, 157), (69, 158), (78, 158), (78, 159), (84, 159), (84, 158), (98, 158), (98, 157), (110, 157), (110, 156), (115, 156), (115, 155), (118, 155),
                 (118, 156), (121, 156), (124, 159), (126, 159), (126, 160), (128, 160), (128, 161), (134, 161), (134, 160), (135, 159), (137, 158), (139, 158), 
                 (140, 157), (141, 156), (145, 156), (146, 155), (159, 155), (159, 154), (161, 154), (162, 153), (171, 153), (172, 154), (178, 154), (178, 153), 
                 (179, 153), (182, 150), (182, 143), (183, 142), (184, 142), (185, 141), (186, 141), (187, 142), (188, 142), (188, 147), (189, 147), (190, 148), 
                 (194, 148), (195, 149), (196, 150), (200, 150), (201, 151), (205, 151), (206, 152), (207, 153), (214, 153), (214, 152), (216, 152), (216, 149), 
                 (217, 148), (217, 147), (219, 147), (219, 150), (220, 150), (221, 151), (222, 151), (223, 152), (237, 152), (237, 151), (238, 150), (238, 148), 
                 (239, 148), (239, 139), (240, 138), (241, 137), (242, 137), (244, 135), (245, 136), (251, 136), (251, 135), (253, 135), (253, 134), (255, 134), 
                 (255, 133), (257, 133), (257, 132), (259, 132), (259, 131), (261, 131), (261, 130), (263, 130), (263, 129), (265, 129), (265, 128), (267, 128), 
                 (267, 127), (268, 126), (269, 125), (270, 124), (270, 123), (271, 122), (271, 121), (272, 120), (272, 118), (273, 117), (273, 116), (274, 115), 
                 (274, 114), (275, 113), (276, 113), (277, 114), (278, 114), (279, 115), (280, 115), (281, 116), (282, 116), (283, 117), (284, 117), (285, 118), 
                 (289, 118), (290, 119), (299, 119), (300, 119), (300, 180)]
ocean_codes = [Path.MOVETO] + [Path.LINETO] * (len(ocean_vertices) - 1) + [Path.CLOSEPOLY]
ocean_path_vertices = ocean_vertices + [ocean_vertices[0]]
ocean_path = Path(ocean_path_vertices, ocean_codes)
ocean_patch = PathPatch(ocean_path, facecolor = 'white', edgecolor = 'gray', alpha = 0.6)

forest_river_vertices = [(61, 141), (61, 136), (62, 135), (63, 135), (64, 134), (65, 134), (65, 133), (68, 133), (68, 132), (71, 132), (71, 131), (72, 130), (73, 130), 
                        (74, 129), (76, 129), (77, 128), (80, 128), (80, 127), (83, 127), (83, 126), (87, 126), (87, 125), (89, 125), (90, 126), (93, 126), (94, 125), 
                        (95, 125), (98, 122), (100, 122), (100, 121), (103, 121), (104, 120), (117, 120), (118, 119), (126, 119), (127, 118), (140, 118), (140, 117), 
                        (142, 117), (142, 124), (138, 124), (137, 123), (130, 123), (129, 122), (125, 122), (124, 123), (120, 123), (119, 124), (117, 124), (115, 125), 
                        (107, 125), (103, 129), (100, 129), (99, 130), (98, 130), (97, 129), (91, 129), (88, 131), (88, 132), (89, 133), (89, 142), (88, 143), (88, 145), 
                        (87, 146), (87, 148), (86, 149), (85, 149), (84, 150), (81, 150), (81, 149), (79, 147), (78, 147), (73, 144), (66, 144), (63, 141)]
forest_river_codes = [Path.MOVETO] + [Path.LINETO] * (len(forest_river_vertices) - 1) + [Path.CLOSEPOLY]
forest_river_path_vertices = forest_river_vertices + [forest_river_vertices[0]]
forest_river_path = Path(forest_river_path_vertices, forest_river_codes)
forest_river_patch = PathPatch(forest_river_path, facecolor = 'white', edgecolor = 'gray', alpha = 0.6)

town_river_vertices = [(142, 117), (155, 117), (156, 118), (158, 118), (159, 119), (161, 119), (163, 121), (166, 121), (167, 122), (169, 122), (170, 123), (181, 123), 
                       (182, 122), (191, 122), (192, 121), (197, 121), (198, 122), (200, 122), (202, 120), (202, 113), (201, 112), (201, 111), (199, 109), (199, 107), 
                       (200, 106), (200, 104), (205, 99), (205, 97), (206, 96), (206, 95), (203, 92), (202, 92), (201, 91), (199, 89), (199, 87),
                       (204, 87), (209, 92), (209, 98), (208, 99), (208, 101), (205, 104), (205, 106), (204, 107), (204, 108), (207, 111), (207, 121), (208, 122), (209, 123), 
                       (211, 123), (215, 127), (215, 128), (217, 130), (217, 131), (218, 132), (218, 133), (219, 134), (219, 145), (217, 145), (217, 136), (215, 134), (214, 130),
                       (213, 129), (212, 128), (211, 129), (210, 130), (207, 127), (207, 125), (204, 122), (201, 125), (200, 125), (199, 126), (199, 124), (194, 124), (192, 126), 
                       (185, 126), (183, 128), (182, 129), (181, 129), (180, 128), (169, 128), (168, 127), (167, 126), (160, 126), (159, 125), (154, 125), (153, 124), (147, 124), 
                       (146, 125), (143, 125), (142, 124)]
town_river_codes = [Path.MOVETO] + [Path.LINETO] * (len(town_river_vertices) - 1) + [Path.CLOSEPOLY]
town_river_path_vertices = town_river_vertices + [town_river_vertices[0]]
town_river_path = Path(town_river_path_vertices, town_river_codes)
town_river_patch = PathPatch(town_river_path, facecolor = 'white', edgecolor = 'gray', alpha = 0.6)

mountain_lake_vertices = [(199, 84), (199, 83), (198, 82), (198, 78), (200, 76), (203, 76), (204, 75), (205, 74), (207, 74), (212, 69), (212, 65), (213, 64), (213, 59), 
                          (215, 57), (215, 54), (214, 53), (214, 50), (213, 49), (213, 45), (209, 41), (207, 41), (206, 40), (205, 41), (204, 40), (203, 39), (203, 37), 
                          (200, 34), (198, 34), (198, 32), (199, 31), (206, 31), (207, 32), (209, 32), (210, 33), (212, 33), (213, 34), (217, 34), (219, 35), (221, 35), 
                          (222, 36), (224, 36), (227, 33), (229, 33), (229, 34), (226, 37), (221, 37), (221, 38), (223, 40), (223, 46), (222, 46), (221, 47), (220, 48), 
                          (219, 46), (218, 46), (217, 47), (217, 50), (218, 51), (218, 56), (217, 57), (217, 60), (216, 61), (216, 63), (215, 64), (215, 72), (213, 74), 
                          (212, 74), (210, 76), (209, 76), (208, 77), (207, 77), (206, 78), (204, 78), (202, 80), (202, 82), (204, 84)]
mountain_lake_codes = [Path.MOVETO] + [Path.LINETO] * (len(mountain_lake_vertices) - 1) + [Path.CLOSEPOLY]
mountain_lake_path_vertices = mountain_lake_vertices + [mountain_lake_vertices[0]]
mountain_lake_path = Path(mountain_lake_path_vertices, mountain_lake_codes)
mountain_lake_patch = PathPatch(mountain_lake_path, facecolor = 'white', edgecolor = 'gray', alpha = 0.6)

def on_sidebar_hover(event):
    global current_tooltip
    tooltip_found = False

    for ax_i, info in zip(axes, images_info):

        ax_i.zorder = 6

        if event.inaxes == ax_i:
            tooltip_found = True
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                if selected_price_type == 'Standard Price':
                    prices = info['standard_prices']
                elif selected_price_type == 'Fisher Price':
                    prices = info['fisher_prices']
                elif selected_price_type == 'Angler Price':
                    prices = info['angler_prices']

                tooltip_texts = [TextArea(info['tooltip_text'], textprops = dict(size = 12, ha = "left", va = "baseline"))]
                price_texts = [TextArea("Price:", textprops = dict(color = 'black', size = 12, ha = "left", va = "baseline"))]

                for i, price in enumerate(prices):
                    color = price_colors[i % len(price_colors)]
                    price_texts.append(TextArea(" " + price, textprops=dict(color = color, size = 12, ha = "left", va = "baseline")))

                    if i < 3:
                        price_texts.append(TextArea(",", textprops = dict(color = 'black', size = 12, ha = "left")))

                price_box = HPacker(children = price_texts, align = "left")
                all_texts = tooltip_texts + [price_box]
                tooltip_box = VPacker(children = all_texts, align = "left", pad = 5)

                tooltip_annotation = AnnotationBbox(
                    tooltip_box, 
                    (x, y), 
                    xybox=(50, 50), 
                    xycoords='data', 
                    boxcoords='offset points', 
                    frameon=True, 
                    pad=0.5
                )

                ax_i.zorder = 10

                if "Forest Pond" in info['location']:
                     pond_patch.set_visible(True)
                else:
                     pond_patch.set_visible(False)

                if "Ocean" in info['location']:
                    ocean_patch.set_visible(True)
                else:
                    ocean_patch.set_visible(False)

                if "Forest River" in info['location']:
                    forest_river_patch.set_visible(True)
                else:
                    forest_river_patch.set_visible(False)

                if "Town River" in info['location']:
                    town_river_patch.set_visible(True)
                else:
                    town_river_patch.set_visible(False)

                if "Mountain Lake" in info['location']:
                    mountain_lake_patch.set_visible(True)
                else:
                     mountain_lake_patch.set_visible(False)

                if current_tooltip is not None:
                    current_tooltip.set_visible(False)
                    current_tooltip.remove()

                ax_i.add_artist(tooltip_annotation)
                current_tooltip = tooltip_annotation
                tooltip.set_visible(True)
                event.canvas.draw_idle()

    if not tooltip_found and current_tooltip is not None:

        pond_patch.set_visible(False)
        ocean_patch.set_visible(False)
        forest_river_patch.set_visible(False)
        town_river_patch.set_visible(False)
        mountain_lake_patch.set_visible(False)

        current_tooltip.set_visible(False)
        current_tooltip.remove()
        current_tooltip = None
        event.canvas.draw_idle()

def on_fish_hover(event):
    global current_tooltip
    tooltip_found = False

    for ax_i, info in fish_axes_data.items():
        ax_i.zorder = 6

    for ax_i, info in fish_axes_data.items():

        if event.inaxes == ax_i:
            tooltip_found = True
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:

                if selected_price_type == 'Standard Price':
                    prices = info['standard_prices']
                elif selected_price_type == 'Fisher Price':
                    prices = info['fisher_prices']
                elif selected_price_type == 'Angler Price':
                    prices = info['angler_prices']

                tooltip_texts = [TextArea(info['tooltip_text'], textprops = dict(size = 12, ha = "left", va = "baseline"))]
                price_texts = [TextArea("Price:", textprops = dict(color = 'black', size = 12, ha = "left", va = "baseline"))]

                for i, price in enumerate(prices):
                    color = price_colors[i % len(price_colors)]
                    price_texts.append(TextArea(" " + price, textprops=dict(color = color, size = 12, ha = "left", va = "baseline")))
                    if i < 3:
                        price_texts.append(TextArea(",", textprops = dict(color = 'black', size = 12, ha = "left")))

                price_box = HPacker(children = price_texts, align = "left")
                all_texts = tooltip_texts + [price_box]
                tooltip_box = VPacker(children = all_texts, align = "left", pad = 5)
                
                tooltip_annotation = AnnotationBbox(tooltip_box, (x, y), xybox = (50, 50), xycoords = 'data', boxcoords = 'offset points', frameon = True, pad = 0.5, zorder = 10)
                
                ax_i.zorder = 10

                if current_tooltip is not None:
                    current_tooltip.set_visible(False)
                    current_tooltip.remove()

                ax_i.add_artist(tooltip_annotation)
                current_tooltip = tooltip_annotation
                event.canvas.draw_idle()
                return

    if not tooltip_found and current_tooltip is not None:
        current_tooltip.set_visible(False)
        current_tooltip.remove()
        current_tooltip = None
        event.canvas.draw_idle()

def on_patch_click(event):
    global fish_axes, fish_rectangle, current_tooltip

    patches = {
        'Pond': pond_patch,
        'Ocean': ocean_patch,
        'Forest River': forest_river_patch,
        'Town River': town_river_patch,
        'Mountain Lake': mountain_lake_patch
        }

    for name, patch in patches.items():
        if patch.contains_point((event.x, event.y)):
            show_fish_images(name, event.x / fig.dpi, event.y / fig.dpi)
            return

    for ax in fish_axes:
        ax.remove()
    
    fish_axes = []

    if fish_rectangle is not None:
        fig.patches.remove(fish_rectangle)
        fish_rectangle = None

    if current_tooltip is not None:
        current_tooltip.set_visible(False)
        current_tooltip.remove()
        current_tooltip = None

    fig.canvas.draw_idle()

def show_fish_images(patch_name, x_pos, y_pos):
    global fish_axes, fish_rectangle, current_tooltip, fish_axes_data

    for ax in fish_axes:
        ax.remove()
        
    fish_axes = []

    if fish_rectangle is not None:
        fig.patches.remove(fish_rectangle)
        fish_rectangle = None

    if current_tooltip is not None:
        current_tooltip.set_visible(False)
        current_tooltip.remove()
        current_tooltip = None

    filtered_images = [
        info for info in full_images_info
        if patch_name in info['location']
    ]

    fig_width, fig_height = fig.get_size_inches()
    norm_x = x_pos / fig_width
    norm_y = y_pos / fig_height

    fish_axes = []
    fish_axes_data = {}

    num_images = len(filtered_images)
    images_per_row = 5
    image_width = 0.05
    image_height = 0.05

    rows = (num_images // images_per_row) + (1 if num_images % images_per_row > 0 else 0)

    x_start = norm_x - (images_per_row / 2) * image_width
    y_start = norm_y - rows * (image_height + 0.02)
    x_start = max(0, min(x_start, 1 - image_width * images_per_row))
    y_start = max(0, min(y_start, 1 - image_height * rows))

    rect_width = min(image_width / 1.5 * images_per_row, 1 - x_start)
    rect_height = image_height * rows

    fish_rectangle = patches.Rectangle((x_start, y_start + 0.05), rect_width + 0.015, rect_height * 1.5, transform = fig.transFigure, color = 'white', alpha = 0.6, zorder = 5)
    fig.patches.append(fish_rectangle)

    for i, info in enumerate(filtered_images):
        row = i // images_per_row
        col = i % images_per_row

        y_start = norm_y - row * (image_height + 0.02)

        ax_i = fig.add_axes([x_start + col * image_width / 1.5, y_start, image_width, image_height])
        image = mpimg.imread(info['path'])
        ax_i.imshow(image)
        ax_i.axis("off")
        ax_i.zorder = 6
        fish_axes_data[ax_i] = info

        fish_axes.append(ax_i)

    fig.canvas.mpl_connect("motion_notify_event", on_fish_hover)

    fig.canvas.draw_idle()


def update_price_type(label):
    global selected_price_type
    selected_price_type = label
    fig.canvas.draw_idle()

def update_season(label):
    global selected_season, images_info, current_tooltip

    selected_season = label

    map_location = "assets\\" + selected_season + ".png"
    map_image = mpimg.imread(map_location)
    map_ax.imshow(map_image, origin="upper")

    visible_locations = [loc for loc, state in location_states.items() if state]

    if visible_locations:
        filtered_images = [
            info for info in full_images_info
            if all(loc in info['location'] for loc in visible_locations) and selected_season in info['season']
        ]
    else:
        filtered_images = [
            info for info in full_images_info
            if selected_season in info['season']
        ]

    images_info = filtered_images

    if current_tooltip is not None:
        current_tooltip.set_visible(False)
        current_tooltip.remove()
        current_tooltip = None

    update_display(filtered_images)

def update_locations(label):
    global images_info, current_tooltip

    location_states[label] = not location_states[label]

    visible_locations = [loc for loc, state in location_states.items() if state]

    if visible_locations:
        filtered_images = [
            info for info in full_images_info
            if all(loc in info['location'] for loc in visible_locations) and selected_season in info['season']
        ]
    else:
        filtered_images = [
            info for info in full_images_info
            if selected_season in info['season']
        ]

        if 'Forest Pond' in visible_locations:
            pond_patch.set_visible(True)
        else:
            pond_patch.set_visible(False)

        if 'Ocean' in visible_locations:
            ocean_patch.set_visible(True)
        else:
            ocean_patch.set_visible(False)

        if 'Forest River' in visible_locations:
            forest_river_patch.set_visible(True)
        else:
            forest_river_patch.set_visible(False)

        if 'Town River' in visible_locations:
            town_river_patch.set_visible(True)
        else:
            town_river_patch.set_visible(False)

        if 'Mountain Lake' in visible_locations:
            mountain_lake_patch.set_visible(True)
        else:
            mountain_lake_patch.set_visible(False)

    images_info = filtered_images

    if current_tooltip is not None:
        current_tooltip.set_visible(False)
        current_tooltip.remove()
        current_tooltip = None

    update_display(filtered_images)

def update_display(filtered_images):

    for ax in axes:
        ax.clear()
        ax.axis("off")

    for i, info in enumerate(filtered_images):
        if i < len(axes):
            image = mpimg.imread(info['path'])
            axes[i].imshow(image)
            axes[i].axis("off")
            axes[i].set_visible(True)

    for i in range(len(filtered_images), len(axes)):
        axes[i].set_visible(False)

    fig.canvas.draw_idle()

def update_scroll(slider_position):
    scroll_position = slider_position - (image_height * num_images)
    offset = scroll_position / num_images

    for i, ax_i in enumerate(axes):
        ax_i.set_position([0.335, 0.975 - (i + 1 + offset) * image_height / num_images, 0.045, image_height / num_images])
    fig.canvas.draw_idle()

if __name__ == "__main__":

    dataframe = pd.read_excel("assets\\fishdata.xlsx")

    images_info = []
    for index, fish in dataframe.iterrows():

        name = "Name: " + fish['Name'] + "\n"
        description = "Description: " + fish['Description'] + "\n"
        time = "Time: " + fish['Time'] + "\n"
        weather = "Weather: " + fish['Weather'] + "\n"
        size = "Size: " + fish['Size'] + " inches\n"
        difficulty = "Difficulty: " + str(fish['Difficulty']) + "\n"
        behavior = "Behavior: " + fish['Behavior']

        standard_prices = []
        fisher_prices = []
        angler_prices = []

        standard_price = fish['Standard Price']
        fisher_price = fish['Fisher Price']
        angler_price = fish['Angler Price']

        for _ in range(4):
            if '|' in standard_price:
                price, standard_price = standard_price.split('|', 1)
                standard_prices.append(price.strip())
            else:
                standard_prices.append(standard_price)

            if '|' in fisher_price:
                price, fisher_price = fisher_price.split('|', 1)
                fisher_prices.append(price.strip())
            else:
                fisher_prices.append(fisher_price)

            if '|' in angler_price:
                price, angler_price = angler_price.split('|', 1)
                angler_prices.append(price.strip())
            else:
                angler_prices.append(angler_price)

        location_list = fish['Location']
        location = "Locations: " + location_list.replace("|", ", ") + "\n"

        season_list = fish['Season']
        season = "Seasons: " + season_list.replace("|", ", ") + "\n"

        tooltip_text = name + description + location + time + season + weather + size + difficulty + behavior

        image_location = "assets\\" + fish['Name'] + ".png"
        images_info.append({"path": image_location, "tooltip_text": tooltip_text, "standard_prices": standard_prices, "fisher_prices": fisher_prices, "angler_prices": angler_prices, "location": fish['Location'], "season": fish['Season']})

    full_images_info = images_info.copy()

    fig, ax = plt.subplots(figsize = (16, 9), num = 'FishFriend') 
    plt.subplots_adjust(left = -0.1, right = 0.85, top = 0.95, bottom = 0.05)
    ax.axis("off")

    num_images = len(images_info)
    image_height = 1.5
    axes = [fig.add_axes([0.335, 0.975 - (i + 1) * image_height / num_images, 0.045, image_height / num_images]) for i in range(num_images)]

    scroll_ax = fig.add_axes([0.3825, 0.03, 0.01, 0.95], facecolor = "lightgray")
    scroll_slider = Slider(scroll_ax, label = None, valmin = num_images * image_height * (-7.5), valmax = image_height * num_images, valinit = image_height * num_images, orientation = "vertical")
    scroll_slider.valtext.set_visible(False)
    scroll_slider.on_changed(update_scroll)

    price_ax = fig.add_axes([0.8, 0.15, 0.15, 0.15])
    price_ax.zorder = 1
    price_buttons = CustomRadioButtons(price_ax, ('Standard Price', 'Fisher Price', 'Angler Price'), callback = update_price_type)

    season_ax = fig.add_axes([0.4, 0.15, 0.15, 0.15])
    season_ax.zorder = 1
    season_buttons = CustomRadioButtons(season_ax, ('Spring', 'Summer', 'Fall', 'Winter'), callback = update_season)

    water_ax = fig.add_axes([0.6, 0.15, 0.15, 0.15])
    water_buttons = CustomCheckButtons(water_ax, ('Forest Pond', 'Ocean', 'Forest River', 'Town River', 'Mountain Lake'), callback = update_locations)
    water_ax.zorder = 1

    image_artists = []
    fish_tooltips = []
    for ax_i, info in zip(axes, images_info):
        ax_i.axis("off")
        img = mpimg.imread(info['path'])
        artist = ax_i.imshow(img, origin = "upper")
        image_artists.append(artist)

        ybox1 = TextArea("", textprops = dict(size = 12, ha = "left", va = "baseline"))
        tooltip = AnnotationBbox(ybox1, (0.5, 0.5), xybox = (50, 50), xycoords = "axes fraction", boxcoords = "offset points", frameon = False, pad = 0)
        tooltip.set_visible(False)
        ax_i.add_artist(tooltip)
        ax_i.zorder = 5
        fish_tooltips.append(tooltip)

    fig.canvas.mpl_connect("motion_notify_event", on_sidebar_hover)

    map_ax = fig.add_axes([0.2, 0.35, 1.0, 0.625])
    map_ax.axis("off")

    map_location = "assets\\" + selected_season + ".png"
    map_image = mpimg.imread(map_location)
    map_ax.imshow(map_image, origin = "upper")

    map_ax.add_patch(pond_patch)
    map_ax.add_patch(ocean_patch)
    map_ax.add_patch(forest_river_patch)
    map_ax.add_patch(town_river_patch)
    map_ax.add_patch(mountain_lake_patch)

    pond_patch.set_visible(False)
    ocean_patch.set_visible(False)
    forest_river_patch.set_visible(False)
    town_river_patch.set_visible(False)
    mountain_lake_patch.set_visible(False)

    logo_ax = fig.add_axes([-0.075, 0.225, 0.5, 0.5])
    logo_ax.axis("off")
    logo_location = "assets\\Logo.jpg"
    logo_image = mpimg.imread(logo_location)
    logo_ax.imshow(logo_image, origin = "upper")

    fig.canvas.mpl_connect("button_press_event", on_patch_click)

    update_season(selected_season)

    map_ax.set_aspect('equal')
    plt.show()