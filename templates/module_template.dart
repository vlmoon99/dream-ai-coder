class ExampleModule extends Module {
  @override
  void binds(Injector i) {
    i.addLazySingleton<ExampleController>(
        (i) => ExampleController(i.get<ExampleRepository>()));
    i.addLazySingleton<ExampleRepository>((i) => ExampleRepository());
  }

  @override
  void routes(RouteManager r) {
    r.child("/example", child: (context) => ExamplePage());
  }
}
