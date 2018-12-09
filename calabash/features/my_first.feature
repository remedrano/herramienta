Feature: Mileage feature

  Scenario: Crear Fillup
    Given I press "Fillup"
    When I take a screenshot
    When I enter "123" into input field number 1
    And I enter "123" into input field number 2
    And I enter "123" into input field number 3
    And I enter "Comentario prueba" into input field number 4
    When I take a screenshot
    Given I press "Save Fillup"

  Scenario: Agregar nuevo vehiculo
    Given I press "Vehicles"
    When I take a screenshot
    Then I press the menu key
    Then I press "Add new vehicle"
    When I enter "Titulo vehiculo" into input field number 1
    And I enter "2018" into input field number 2
    And I enter "Hecho en china" into input field number 3
    And I enter "modelo 2019" into input field number 4
    And I enter "Descripcion" into input field number 5
    When I take a screenshot
    Given I press "Add new vehicle"
  
  Scenario: Ver estadisticas
    Given I press "Statistics"
    When I take a screenshot

  Scenario: Ver Historial
     Given I press "History"
    When I take a screenshot