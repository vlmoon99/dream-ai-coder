//Local Repository for Secure Storage using Flutter secure Storage
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:convert';
import 'template_model.dart';

class SecureStorageRepository {
  final FlutterSecureStorage secureStorage = FlutterSecureStorage();

  /// Save the TemplateModel to secure storage.
  Future<void> saveModel(TemplateModel model) async {
    String jsonString = jsonEncode(model.toJson());
    await secureStorage.write(key: 'template_model', value: jsonString);
  }

  /// Load the TemplateModel from secure storage.
  Future<TemplateModel?> loadModel() async {
    String? jsonString = await secureStorage.read(key: 'template_model');
    if (jsonString == null) return null;
    Map<String, dynamic> jsonData = jsonDecode(jsonString);
    return TemplateModel.fromJson(jsonData);
  }

  /// Delete the TemplateModel from secure storage.
  Future<void> deleteModel() async {
    await secureStorage.delete(key: 'template_model');
  }
}

//Local Repository for non-encrypted data using Hive
import 'package:hive/hive.dart';
import 'template_model.dart';

class HiveStorageRepository {
  final String boxName = 'templateBox';

  /// Initialize Hive and open a box.
  Future<void> init() async {
    await Hive.openBox<TemplateModel>(boxName);
  }

  /// Save the TemplateModel to Hive storage.
  Future<void> saveModel(TemplateModel model) async {
    var box = Hive.box<TemplateModel>(boxName);
    await box.put('template_model', model);
  }

  /// Load the TemplateModel from Hive storage.
  Future<TemplateModel?> loadModel() async {
    var box = Hive.box<TemplateModel>(boxName);
    return box.get('template_model');
  }

  /// Delete the TemplateModel from Hive storage.
  Future<void> deleteModel() async {
    var box = Hive.box<TemplateModel>(boxName);
    await box.delete('template_model');
  }
}

//Firebase Firestore repositroy for Firebase Database storage for non-encrypted data
import 'package:cloud_firestore/cloud_firestore.dart';
import 'template_model.dart';

class FirestoreRepository {
  final CollectionReference collection =
      FirebaseFirestore.instance.collection('templateModels');

  /// Save the TemplateModel to Firestore.
  Future<void> saveModel(TemplateModel model) async {
    await collection.doc('template_model').set(model.toJson());
  }

  /// Load the TemplateModel from Firestore.
  Future<TemplateModel?> loadModel() async {
    DocumentSnapshot doc = await collection.doc('template_model').get();
    if (doc.exists) {
      return TemplateModel.fromJson(doc.data() as Map<String, dynamic>);
    }
    return null;
  }

  /// Delete the TemplateModel from Firestore.
  Future<void> deleteModel() async {
    await collection.doc('template_model').delete();
  }
}
