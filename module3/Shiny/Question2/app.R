# author: Uliana Plotnikova
# Class: Data 608
# Data can be found here:
# https://github.com/charleyferrari/CUNY_DATA608/tree/master/module3/data



library(ggplot2)
library(dplyr)
library(plotly)
library(shiny)
library(shinyWidgets)


df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")


each_state <- df %>% select(ICD.Chapter, Year, Crude.Rate, State)
nation<- df %>% select(ICD.Chapter, Year, State, Deaths, Population, Crude.Rate) %>%  mutate(Crude.Rate = round((sum(Deaths) / sum(Population)) * 10^5, 1))
nation_ave <- nation %>%
  select(ICD.Chapter, Year, Crude.Rate, State) %>%
  mutate(State = "National_Ave") %>%
  group_by(ICD.Chapter, Year)


total <- union_all(each_state, nation_ave)


ui <- fluidPage(
  sidebarPanel(
    selectInput('State', 'State', unique(total$State), selected='NY'),
    selectInput('ICD.Chapter', 'Cause', unique(total$ICD.Chapter), selected='Neoplasms')
  ),
  setBackgroundColor(color = c("#F7FBFF", "#2171B5"),
                     gradient = "linear",
                     direction = "bottom"),
  titlePanel("State Mortality Rate VS National Average"),
  mainPanel(width=10,
            plotlyOutput('plot1')
  )
)

server <- function(input, output, session) {
  
  nationalData <- reactive({
    nation_ave %>%
      filter(ICD.Chapter == input$ICD.Chapter)
  })
  
  statedata <- reactive({
    df <- total %>%
      filter(State == input$State, ICD.Chapter == input$ICD.Chapter)
  })
  
  combined  <- reactive({
    merge(x = nationalData(), y = statedata(), all = TRUE)
  })
  
  output$plot1 <- renderPlotly({
    
    df <- total %>%
      filter(State == input$State, ICD.Chapter == input$ICD.Chapter)
    
    plot_ly(combined(), x = ~Year, y = ~Crude.Rate, color = ~State, type='scatter',
            mode = 'markers+lines', line = list(color = '#17BECF'))
  })
  
}

shinyApp(ui,server)
