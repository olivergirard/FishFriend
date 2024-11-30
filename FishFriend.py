import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mcolors
import pandas as pd
import array as arr

from matplotlib.offsetbox import AnnotationBbox, TextArea, VPacker, HPacker
from matplotlib.widgets import Slider, RadioButtons

price_colors = ['black', 'gray', 'gold', 'darkviolet']

selected_price_type = 'Standard Price'
selected_season = 'Spring'

current_tooltip = None

def on_sidebar_hover(event):
    global current_tooltip
    tooltip_found = False

    for ax_i, tooltip in zip(axes, tooltips):
        if event.inaxes == ax_i:
            tooltip_found = True
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                
                info = images_info[axes.index(ax_i)]
                if selected_price_type == 'Standard Price':
                    prices = info['standard_prices']
                elif selected_price_type == 'Fisher Price':
                    prices = info['fisher_prices']
                elif selected_price_type == 'Angler Price':
                    prices = info['angler_prices']

                tooltip_texts = [TextArea(info["tooltip_text"], textprops = dict(size = 12, ha = "left", va = "baseline"))]
                price_texts = [TextArea("Price:", textprops = dict(color = 'black', size = 12, ha = "left", va = "baseline"))]

                for i, price in enumerate(prices):
                    color = price_colors[i % len(price_colors)]
                    price_texts.append(TextArea(" " + price, textprops = dict(color = color, size = 12, ha = "left", va = "baseline")))

                    if i < 3:
                        price_texts.append(TextArea(",", textprops = dict(color = 'black', size = 12, ha = "left")))

                price_box = HPacker(children=price_texts, align = "left")
                all_texts = tooltip_texts + [price_box]
                tooltip_box = VPacker(children = all_texts, align = "left", pad = 5)

                tooltip_annotation = AnnotationBbox(tooltip_box, (0.5, 0.5), xybox = (50, 50), xycoords = 'axes fraction', boxcoords = 'offset points', frameon = True, pad = 0.5)

                if current_tooltip is not None:
                    current_tooltip.set_visible(False)
                    current_tooltip.remove()

                ax_i.zorder = 10
                ax_i.add_artist(tooltip_annotation)
                current_tooltip = tooltip_annotation
                tooltip.set_visible(True)
                event.canvas.draw_idle()

    if not tooltip_found and current_tooltip is not None:
        current_tooltip.set_visible(False)
        event.canvas.draw_idle()

def update_price_type(label):
    global selected_price_type
    selected_price_type = label
    fig.canvas.draw_idle()

def update_season(label):
    global selected_season
    selected_season = label

    map_location = "assets\\" + selected_season + ".png"
    map_image = mpimg.imread(map_location)
    map_ax.imshow(map_image, origin = "upper")

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
        images_info.append({"path": image_location, "tooltip_text": tooltip_text, "standard_prices": standard_prices, "fisher_prices": fisher_prices, "angler_prices": angler_prices})

    fig, ax = plt.subplots(figsize = (16, 9)) 
    plt.subplots_adjust(left = 0.1, right = 0.85, top = 0.95, bottom = 0.05)
    ax.axis("off")

    num_images = len(images_info)
    image_height = 1.5
    axes = [fig.add_axes([0.335, 0.975 - (i + 1) * image_height / num_images, 0.045, image_height / num_images]) for i in range(num_images)]

    scroll_ax = fig.add_axes([0.3825, 0.03, 0.01, 0.95], facecolor = "lightgray")
    scroll_slider = Slider(scroll_ax, label = None, valmin = num_images * image_height * (-7.5), valmax = image_height * num_images, valinit = image_height * num_images, orientation = "vertical")
    scroll_slider.valtext.set_visible(False)
    scroll_slider.on_changed(update_scroll)

    price_ax = fig.add_axes([0.825, 0.15, 0.15, 0.15])
    price_ax.zorder = 10
    price_buttons = RadioButtons(price_ax, ('Standard Price', 'Fisher Price', 'Angler Price'))

    for r in price_buttons.labels: 
        r.set_fontsize(12)

    price_buttons.on_clicked(update_price_type)

    season_ax = fig.add_axes([0.425, 0.15, 0.15, 0.15])
    season_ax.zorder = 10
    season_buttons = RadioButtons(season_ax, ('Spring', 'Summer', 'Fall', 'Winter'))

    for r in season_buttons.labels: 
        r.set_fontsize(12)

    season_buttons.on_clicked(update_season)

    image_artists = []
    tooltips = []
    for ax_i, info in zip(axes, images_info):
        ax_i.axis("off")
        img = mpimg.imread(info["path"])
        artist = ax_i.imshow(img, origin = "upper")
        image_artists.append(artist)

        ybox1 = TextArea("", textprops = dict(size = 12, ha = "left", va = "baseline"))
        tooltip = AnnotationBbox(ybox1, (0.5, 0.5), xybox = (50, 50), xycoords = "axes fraction", boxcoords = "offset points", frameon = False, pad = 0)
        tooltip.set_visible(False)
        ax_i.add_artist(tooltip)
        ax_i.zorder = 5
        tooltips.append(tooltip)

    fig.canvas.mpl_connect("motion_notify_event", on_sidebar_hover)

    map_ax = fig.add_axes([0.2, 0.35, 1.0, 0.625])
    map_ax.axis("off")

    map_location = "assets\\" + selected_season + ".png"
    map_image = mpimg.imread(map_location)
    map_ax.imshow(map_image, origin = "upper")

    plt.show()

### TODO: Pick up at Week 4 in Final Project Proposal. This involves:
###           - Creating axes for bodies of water. If I can map out the body of water by its pixels in Procreate and then make an axis out of that, this is preferable.
###           - Creating tooltips for bodies of water that involve more fish images. Expect lots of VPacker and HPacker logic.
###           - Reapplying the logic of on_sidebar_hover to the new axes in the image tooltip. This is probably best done in another function.

### TODO: The visualization still needs a cool logo.
