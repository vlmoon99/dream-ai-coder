# Dream AI Coder Console App

This is a console application that helps generate code projects using a language model. The application guides users through creating and managing projects based on their requirements.

## Features

- Select development environment (e.g., Flutter/Dart, Java/Spring)
- Define project requirements
- Progress through defined project stages
- Automatic code generation and transformation

## How to use


1. In order to generate code you need to have :

1.Technology model, each project use technology model inside,
also each technology contains stages which user need to pass in order to generate project, 

```
curl -X POST http://localhost:3333/create-technology \
     -H "Content-Type: application/json" \
     -d '{
           "technology": "Flutter",
           "stages": 3
          }'
```

2.After you create the technology , you need to create stages for this technology, each stage will
contains the description and template for LLM in order to generate code for customer

```
curl -X POST http://localhost:3333/create-template \
     -H "Content-Type: application/json" \
     -d '{
	   "author" : "root",
           "technology": "Flutter",
           "stage": 1,
           "template": "your template for LLM in order to generate code",
           "example": "your example for LLM",
           "description": "Entity Modeling, Models and Repository creating , connect entities with each others , describe this connection with entities. Connect Firebase to the App"
         }'

```

3.After you will have your technology + tempaltes done , you need to create test project in order to test your idea

```

curl -X POST http://localhost:3333/create-project \
-H "Content-Type: application/json" \
-d '{"name": "AI Trainer","technology": "Flutter"}'

```

4.After your project was created you need to start generate your code and project files using LLM,


## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd dream-ai-coder
