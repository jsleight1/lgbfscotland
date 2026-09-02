## Introduction

Lgbfscotland uses the transformed data (see [data workflow](data_workflow.md))
to create a series of `Indicator Area` and `Indicator` class objects that
are used to summarise and present LGBF data across the shiny application.

## Indicator

The object that acts as the lowest common denominator is the `indicator` class
object. This object stores data for a single indicator for a single local
authority.

An example of this object can be created.

```
output = indicator.example_indicator()
output
```

This object has associated attributes storing the id, title, authority and
category of the stored indicator data set.

```
output.data
output.id()
output.title()
output.authority()
output.category()
```

The object can be plotted and summarised.

```
output.plot(type = "indicator")
output.plot(type = "numerator_denominator")
output.summary(type = "indicator")
```

The object can also be included in a shiny application with its associated
`mod_ui` and `mod_server` methods.

```
app_ui = ui.page_navbar(
    output.mod_ui("indicator", object = output)
)

def server(input, output, session):
    output.mod_server("indicator", object = output)

App(ui=app_ui, server=server)
```

## Indicator Area

lgbfscotland also contains functionality that combines several indicators into
a single indicator area. A list of `indicator` objects can be stored
in a `indicator_area` object.

An example of this object can be created

```
data = indicator.example_indicator()
output = indicator_area(data = [data], id = "area")
output
```

Appropriate getter methods can be called to obtain this objects attributes

```
output.data
output.id
```

Similarly to the `indicator` object, the `indicator_area` object can be included
in a shiny application with its associated `mod_ui` and `mod_server` methods.

```
app_ui = ui.page_navbar(
    output.mod_ui("indicator_area", object = output)
)

def server(input, output, session):
    output.mod_server("indicator_area", object = output)

App(ui=app_ui, server=server)
```
