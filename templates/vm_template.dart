import 'package:rxdart/rxdart.dart';

/// State management class for the ViewModel.
/// Modify this to match your specific state.
class VMState {
  final String data;
  final bool isLoading;
  final String? error;

  VMState({
    this.data = '',
    this.isLoading = false,
    this.error,
  });

  /// Create a copy of the state with optional overrides.
  VMState copyWith({
    String? data,
    bool? isLoading,
    String? error,
  }) {
    return VMState(
      data: data ?? this.data,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }

  @override
  String toString() {
    return 'VMState(data: $data, isLoading: $isLoading, error: $error)';
  }
}

/// ViewModel class managing state and connecting to services and repositories.
class MyViewModel {
  final BehaviorSubject<VMState> streamController =
      BehaviorSubject<VMState>.seeded(VMState());

  /// Exposing the stream for the UI to subscribe to (StreamBuilder).
  Stream<VMState> get stream => streamController.stream;

  /// Exposing the current state value.
  VMState get state => streamController.value;

  MyRepository repository;
  MyService service;

  /// Constructor injecting necessary services and repositories.
  MyViewModel(this.repository, this.service);

  /// Initialize the ViewModel, performing any initial actions.
  void init() {
    updateState(isLoading: true);
    // Example: Load data on init
    fetchData();
  }

  /// Method to fetch data from the repository or service.
  Future<void> fetchData() async {
    try {
      updateState(isLoading: true);

      // Call the repository/service and handle the response
      final data = await repository.getData(); // Or service.getData()

      updateState(data: data, isLoading: false);
    } catch (error) {
      updateState(isLoading: false, error: error.toString());
    }
  }

  /// Helper function to update the state reactively.
  void updateState({
    String? data,
    bool? isLoading,
    String? error,
  }) {
    final newState = state.copyWith(
      data: data,
      isLoading: isLoading,
      error: error,
    );
    streamController.add(newState);
  }

  /// Dispose the stream controller to avoid memory leaks.
  void dispose() {
    streamController.close();
  }
}
