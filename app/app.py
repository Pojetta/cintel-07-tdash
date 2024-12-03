import seaborn as sns  # For creating plots
from faicons import icon_svg  # Provides access to icon assets for UI

from shiny import reactive  # Enables reactive programming
from shiny.express import input, render, ui  # Simplifies Shiny UI and server definitions
import palmerpenguins  # Dataset for visualizations and analysis
from pathlib import Path  # For working with file system paths



# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

css_file = Path(__file__).parent / "css" / "styles.css"

ui.include_css(css_file)

# Set global options for the UI
ui.page_opts(title="Palmer Penguins", fillable=True)

# Sidebar for filtering and useful links
with ui.sidebar(title="Filters"):
    # Slider to filter penguins by body mass
    ui.input_slider("mass", "Body Mass", 2000, 6000, 6000)
    # Checkbox group to filter by species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Separator line
    ui.hr()
    ui.h6("Links")  # Header for external resources and references
    # Various external links
    ui.a(
        "GitHub Source",
        href="https://github.com/pojetta/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://pojetta.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/pojetta/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Layout with value boxes to display calculated statistics
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), theme=ui.value_box_theme(bg="#1b7978"),class_="text-center"):
        "Number of penguins"

        # Render total count of filtered penguins
        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme=ui.value_box_theme(bg="purple"),class_="text-center"):
        "Average bill length"

        # Render average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), theme=ui.value_box_theme(bg="darkorange"),class_="text-center"):
        "Average bill depth"

        # Render average bill depth
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout with two cards: one for a scatterplot and one for a data table
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Length vs Bill depth", style="color: white; background-color: #2A2A2A;")

        # Scatterplot of bill length vs. bill depth, colored by species
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
                palette={"Adelie": "#1b7978", "Gentoo": "purple", "Chinstrap": "darkorange"}
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin data", style="color: white; background-color: #2A2A2A;")

        # Render data table of filtered penguin data with selected columns
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Optional: Include external CSS for additional styles
# ui.include_css(app_dir / "styles.css")

# Reactive function to filter the dataset based on user input
@reactive.calc
def filtered_df():
    # Filter by species and body mass
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
