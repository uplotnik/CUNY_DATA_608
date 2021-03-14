# author: Uliana Plotnikova
# Class: Data 608
# Data can be found here:
# https://github.com/charleyferrari/CUNY_DATA608/tree/master/module3/data


# Question 1:
#    As a researcher, you frequently compare mortality rates from particular
# causes across different States. You need a visualization that will let you see
# (for 2010 only) the crude mortality rate, across all States, from one cause
# (for example, Neoplasms, which are effectively cancers). Create a visualization
# that allows you to rank States by crude mortality for each cause of death.


library(ggplot2)
library(dplyr)
library(shiny)
library(rsconnect)
library(shinyWidgets)



df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")

ui <- fluidPage( 
  setBackgroundColor(color = c("#F7FBFF", "#2171B5"),
                     gradient = "linear",
                     direction = "bottom"),
  titlePanel('State Moratlity Rate by Cause'),
  sidebarPanel(selectInput('Cause', 'Cause', unique(df$ICD.Chapter),
                           selected='Neoplasms')),
  mainPanel(htmlOutput(outputId = 'selection'),
            plotOutput('plot1', height="auto"),
            h6("The Crude Mortality Rate across all States"))
)

server <- shinyServer(function(input, output, session) {
  selectedData <- reactive({
    df %>% filter(ICD.Chapter == input$Cause & Year == 2010 )
  })
  
  output$selection <- renderText({
    paste('<b> Crude rate for: </b>', input$Cause)
  })
  
  output$plot1 <- renderPlot({
    
    ggplot(selectedData(), aes(x=reorder(State, -Crude.Rate), y=Crude.Rate)) +
      geom_col(fill = "darkgreen") +
      coord_flip() +
      geom_text(aes(label=Crude.Rate),
                size=3,
                hjust=-0.2,
                color="darkgreen") +
      xlab("State") +
      ylab("Crude Rate") +
      theme(panel.background = element_blank())
  }, height = function() {
    session$clientData$output_plot1_width}
  )
})

shinyApp(ui = ui, server = server)
