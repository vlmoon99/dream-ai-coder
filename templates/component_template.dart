import 'package:flutter/material.dart';

/// A generic component template that can be reused for various UI elements.
class MyComponent extends StatelessWidget {
  final String data;
  final VoidCallback onAction; // Callback for triggering ViewModel actions

  /// Constructor for the component, accepting visual input parameters and callbacks
  MyComponent({
    required this.data,
    required this.onAction,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          'Data: $data',
          style: TextStyle(fontSize: 20),
        ),
        SizedBox(height: 20),
        ElevatedButton(
          onPressed: onAction, // Trigger the action via callback
          child: Text('Refresh Data'),
        ),
      ],
    );
  }
}
