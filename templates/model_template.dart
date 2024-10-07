import 'package:json_annotation/json_annotation.dart';

part 'template_model.g.dart';

/// This is a **TemplateModel** intended to serve as a base for generating
/// domain-specific models with generic properties.
@JsonSerializable()
class TemplateModel {
  final String property1;
  final int property2;
  final bool property3;
  final List<String>? property4;
  final Map<String, dynamic>? property5;

  /// Constructor for TemplateModel with generic fields.
  TemplateModel({
    required this.property1,
    required this.property2,
    required this.property3,
    this.property4,
    this.property5,
  });

  /// Factory to create an instance of TemplateModel from JSON data.
  factory TemplateModel.fromJson(Map<String, dynamic> json) =>
      _$TemplateModelFromJson(json);

  /// Method to serialize TemplateModel instance to JSON format.
  Map<String, dynamic> toJson() => _$TemplateModelToJson(this);

  @override
  String toString() {
    return "{property1: $property1, property2: $property2, property3: $property3, property4: $property4, property5: $property5}";
  }

  /// Override equality operator to compare `TemplateModel` objects.
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is TemplateModel &&
          property1 == other.property1 &&
          property2 == other.property2 &&
          property3 == other.property3 &&
          property4 == other.property4 &&
          property5 == other.property5;

  /// Override `hashCode` to generate a unique hash based on properties.
  @override
  int get hashCode =>
      property1.hashCode ^
      property2.hashCode ^
      property3.hashCode ^
      (property4?.hashCode ?? 0) ^
      (property5?.hashCode ?? 0);
}
