import 'package:json_annotation/json_annotation.dart';
part 'user_model.g.dart';

@JsonSerializable()
class User {
  final String id;
  final DateTime createdAt;
  final DateTime updatedAt;
  final int age;

  User({
    required this.id,
    required this.createdAt,
    required this.updatedAt,
    required this.age,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  Map<String, dynamic> toJson() => _$UserToJson(this);

  User copyWith({
    String? id,
    DateTime? createdAt,
    DateTime? updatedAt,
    int? age,
  }) {
    return User(
      id: id ?? this.id,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      age: age ?? this.age,
    );
  }
}