import 'package:flutter/material.dart';

class MyPage extends StatefulWidget {
  @override
  _MyPageState createState() => _MyPageState();
}

class _MyPageState extends State<MyPage> {
  late MyViewModel viewModel;

  @override
  void initState() {
    super.initState();

    // Initialize the ViewModel with repository and service
    viewModel = MyViewModel(MyRepository(), MyService());
    viewModel.init(); // Initialize ViewModel actions
  }

  @override
  void dispose() {
    viewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("My Page"),
      ),
      body: StreamBuilder<VMState>(
        stream: viewModel.stream,
        builder: (context, snapshot) {
          final state = snapshot.data;

          // Show loading state or error message
          if (state == null || state.isLoading) {
            return Center(child: CircularProgressIndicator());
          }

          if (state.error != null) {
            return Center(child: Text('Error: ${state.error}'));
          }

          // Pass data and callbacks to components
          return MyComponent(
            data: state.data,
            onAction: () {
              viewModel.fetchData(); // Trigger VM action from the UI
            },
          );
        },
      ),
    );
  }
}
