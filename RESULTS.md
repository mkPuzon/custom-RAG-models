# Model Results
**Overview**: This file evaluates the performance differences between a base model LLM straight from Ollama (qwen3:0.6b) vs. that same base model with a custom ModelFile and access to domain specific data through a RAG system (qwen3-rag:0.6b).

The chosen topic is optic flow and the human visual system since my reserach covered these topics in detail. A smaller langauge model likely has only a rough idea of this area of computational neroscientific research, so it stands as a good example for the possibilities opened up by specialized RAG systems. 

> NOTE: qwen3:0.6b is a "thinking" model. These tokens are not included in the responses below for clarity.


## qwen3:0.6b - Base Model
**Prompt 1**: "Tell me about optic flow and how the primate brain processes it"

**Full Response 1**:
```
Optic flow refers to the visual information processed by the eyes, which allows animals and humans to perceive 
movement and changes in their surroundings. This concept is fundamental for navigation, balance, and perception 
in the environment. The primate brain processes optic flow in several ways: 

1. **Optic Flow Detection**: The eyes detect movement and changes in the environment, which the brain translates 
into visual information. This is critical for tasks like orientation, tracking, and spatial awareness.

2. **Brain Processing**:  
   - In humans, the **superior temporal sulcus** is specifically involved in processing motion and direction.  
   - Other primates, such as great apes, have similar structures but may differ in size or function. For 
example, in chimpanzees, the brain’s role in processing optic flow is more focused on spatial orientation rather 
than complex navigation.  

3. **Applications**:  
   - **Humans**: Optic flow helps with tasks like walking, climbing, and spatial orientation.  
   - **Primates**: In species like apes, it aids in navigation and social interactions, though their processing 
is more about spatial relationships rather than complex dynamic environments.  

In summary, the primate brain processes optic flow to help with navigation, balance, and environmental 
perception, though the specific mechanisms and efficiency vary across species.
```

**Prompt 2**: "Tell me about brain area MSTd and what it responds to"

**Full Response 2**:
```
The **MSTd (cerebellar cortex)** is a part of the **cerebellar cortex**, which is a key component of the **cerebellum** in the brain. The cerebellum 
plays a crucial role in **motor control**, **balance**, and **coordination**. Here's a breakdown of its function and response:

### **Function of the Cerebellar Cortex**
1. **Motor Control**: The cerebellar cortex processes movement signals from the central nervous system (such as those from the spinal cord and 
thalamus) to guide voluntary movements.
2. **Balance and Coordination**: It helps with **vestibular input** (from the inner ear) to maintain **balance** and **dynamic equilibrium**.
3. **Feedback**: The cerebellar cortex provides **motor feedback** to the brain, allowing for adjustments in movement and posture.

### **Response to Movement Signals**
- The cerebellar cortex receives and integrates **movement-related signals** from the spinal cord and sensory systems.
- These signals are used to **guide voluntary actions** and to **adjust motor output** based on sensory feedback.

### **Summary**
The cerebellar cortex (MSTd) is vital for **movement processing**, **balance**, and **coordination**. It processes movement signals to guide motor 
skills and maintain equilibrium, making it a central part of the cerebellum's function.
```

## qwen3-rag:0.6b - Custom Build from ModelFile
**Prompt**: "Tell me about optic flow and how the primate brain processes it"

**Full Response**:
```

```

**Prompt 2**: "Tell me about brain area MSTd and what it responds to"

**Full Response 2**:
```

```

## Detailed Response Comparisions