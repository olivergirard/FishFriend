# FishFriend
FishFriend is an interactive, data-driven application that makes *Stardew Valley* fishing gameplay more efficient and accessible, especially for first-time players. This application helps users visualize data relating to the fish in *Stardew Valley*, including information such as where and when a fish can be caught, how much a fish can sell for, and much more. This application was constructed as a final project for CS43900: Introduction to Data Visualization. It makes use of Python's Matplotlib and Pandas libraries. Any relevant assets and data were collected directly from the [Stardew Valley Wiki](https://stardewvalleywiki.com/Stardew_Valley_Wiki) and compiled into a spreadsheet.

## Execution
FishFriend can be run directly from the included `.sln` file, or from the `FishFriend.exe` file at `FishFriend\dist\FishFriend.exe`.

## Features
### Seasons
Fish can be filtered by season. Only one season can be selected at a time. The map changes color to reflect a change in season.
<p align="center">
  <img src="https://github.com/user-attachments/assets/ecb6a05a-64cf-4047-8fb2-6a2b82603c24?raw=true" alt="Fish can be filtered by season."/>
</p>

### Locations
Fish can be filtered by location. Multiple locations can be selected at a time. Only the fish available in all selected locations will be displayed. The selected locations will be highlighted in light blue on the map.
<p align="center">
  <img src="https://github.com/user-attachments/assets/303d9df0-e417-4c4c-ad60-93061275e68a?raw=true" alt="Fish can be filtered by location."/>
</p>

A location can also be selected to determine what fish can be caught at that location. Further information on these fish can be gathered by hovering over them with the tooltip. I find this to be the most helpful feature within FishFriend.
<p align="center">
  <img src="https://github.com/user-attachments/assets/322d6095-3ae8-48af-8358-e8e4a05ead6d?raw=true" alt="A location can be selected."/>
</p>

### Prices
Fish can be filtered by price depending on a given skill. The price of a fish changes depending on whether a player has no skill, the "Fisher" skill, or the "Angler" skill. Prices are changed within the tooltip that appears whenever a fish icon is hovered over. The different colors of prices correspond to whether a fish is of standard, silver, gold, or iridium quality.
<p align="center">
  <img src="https://github.com/user-attachments/assets/321db560-2199-4c91-a503-da0e205a7fb1?raw=true" alt="A location can be selected."/>
</p>
