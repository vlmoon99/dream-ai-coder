class BusinessLogicService {
  /// Method for applying business logic 1.
  /// Takes InputParamsBusinessLogic1 and returns ResponseBusinessLogic1.
  ResponseBusinessLogic1 businessLogicName1(
      InputParamsBusinessLogic1 inputParams) {
    // Example logic based on inputParams
    print('Applying business logic 1 to: ${inputParams.property1}');

    // Perform your business logic here and generate the response
    String result = "Processed ${inputParams.property1} with logic 1";
    return ResponseBusinessLogic1(result: result);
  }

  /// Method for applying business logic 2.
  /// Takes InputParamsBusinessLogic2 and returns ResponseBusinessLogic2.
  ResponseBusinessLogic2 businessLogicName2(
      InputParamsBusinessLogic2 inputParams) {
    // Example logic based on inputParams
    print('Applying business logic 2 to: ${inputParams.property2}');

    // Perform your business logic here and generate the response
    int result = inputParams.property2 * 2; // Example logic
    return ResponseBusinessLogic2(result: result);
  }
}
