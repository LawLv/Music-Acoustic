# Assignment 1 Literature

Yilai Chen  Article: 《Commuted Piano Synthesis 1995》

## 1. Summary for Commuted Piano Synthesis

The commuted piano synthesis algorithm is a simplified acoustic model of the piano.

The model includes <u>multiple coupled strings</u>, a <u>nonlinear hammer</u>, and an arbitrarily large <u>soundboard</u> and <u>enclosure</u>.

- Strings: The main vibrating part responsible for producing sound.
- Hammers: Used to strike the strings, and their characteristics are nonlinear.
- Soundboard and enclosure: Responsible for the transmission and enhancement of sound.

<u>Nonlinear properties</u>: The hammer is a felt-covered component whose behavior is highly nonlinear.

Through certain mathematical simplifications, the computational complexity is greatly reduced, allowing the algorithm to run on limited hardware resources. In its present form, a complete, two-key piano can be synthesized in real time on a single 25MHz Motorola DSP56001 signal processing chip.

### 1.1 Introduction

Two Core Methods:

- <u>Commutation of Resonating Body</u>:
  The resonating body of the instrument is exchanged with the string model, thus avoiding the complex calculation of high-order digital filters.
  That is, the resonance effect is pre-embedded by pre-convolve the impulse response of the resonating body with the string excitation signal (such as the change in the force of the string being plucked or struck over time).
- <u>Wavetable Method</u>:
  The pre-convolved waveform is stored in the wavetable.
  When synthesizing the sound, just pass the wavetable signal into the string ("played into the string").
  The final sound effect can well restore the natural resonance of the string and the resonating body when the string is plucked or struck.

In this paper, the above techniques are extended to the piano model. The piano model uses a linearized hammer model, which is characterized by the impact of striking velocity.

### 1.2 The piano

A piano is an example of a nonlinear string. When the string is struck, only the velocity of the hammer needs to be controlled as the only variable.

- Modeling of piano <u>strings</u>

  Strings are simple in structure, it is uniform, taut and almost rigidly fixed, highly linear. The digital waveguide method is well suited for modeling a single string. The digital waveguide method is well suited for modeling a single string.
  Adding an all-pass filter to the string loop introduces implementation complexity.
  In this experiment, only the vertical vibration plane of the string is simulated. Only one string is simulated per key.

- Resonator

  The soundboard and shell of a piano involve two-dimensional or three-dimensional waveguide propagation, which requires modeling using a high-dimensional waveguide grid. The computational cost is very high. However, the <u>commuted synthesis technique</u> proposed in this paper records the impulse response of the soundboard/shell, stores its samples in a read-only memory, and directly acts on the strings in combination with the collision dynamics of the hammer and the strings. This method is also applicable to the modeling of all the coordinated vibrating strings when the sustain pedal is pressed, greatly reducing the computational complexity.

- Hammer

  The complexity of piano hammers mainly comes from the felt material they are covered with, which has nonlinear properties that are manifested by a rapid increase in spring constant upon impact. This can lead to complications where the string rebounds after the initial strike and hits the hammer again. This severe nonlinearity prevents the direct application of exchange synthesis techniques.

### 1.3 Commuted Piano Synthesis

​        High fidelity and low computational cost achieved through "interactive piano synthesis". The interaction between hammers and strings is essentially a number of discrete events that occur each time a string is struck. Therefore, the interaction between hammers and strings can be approximated as several discrete impacts that are filtered through a filter that depends on the speed of the hammer-string collision. In the picture, the curve of the striking force shows three peaks, indicating that the hammer is in contact with the string long enough that the string's rebound wave is able to compress the string more than twice before the hammer leaves the string.

<img src="D:\DT2212 Music Acoustic\Assignment1\1" alt="image-20250202143500234" style="zoom: 33%;" />

​        For a string, the amplitude and timing of all interactive impacts can be predicted with a known key number and hammer velocity. If you want to simulate the unpredictability of the force pulse when re-strike the string, you can randomly perturb the amplitude of the interactive impacts according to the vibration amplitude of the string before the strike.

​       <img src="D:\DT2212 Music Acoustic\Assignment1\2" alt="image-20250202144040388" style="zoom: 80%;" />

- #####  Illustrative Implementation

  ​        Next, multiple force pulses are created from multiple impact pulses and applied to the synthesis of the piano strings. The following figure shows this process: Each input pulse (Impulses 1, 2, 3) is first processed through a low-pass filter (LPF1, LPF2, LPF3) to produce a corresponding filtered pulse (δ1, δ2, δ3). These pulses are summed up and input to the piano string model to form the synthesized hammer-string interaction force pulse. As the input pulse amplitude increases, the output pulses become higher and thinner, with less overlap. This means that the force pulses of each impact are more clearly reflected.

  ​        At certain dynamic levels, this model has linear and time-invariant characteristics. That is, different parts of the model (such as the soundboard/shell filter, string and hammer low-pass filters) can be "swapped". This "swapped" operation allows us to combine the soundboard/shell filter with the steel string system and even the hammer low-pass filter, thereby simplifying the system calculation process. The figure 4 and 5 shows the natural order block diagram of the complete piano synthesis system and the results obtained by swapping the interaction of the hammer-string assembly with the soundboard and shell.

<img src="D:\DT2212 Music Acoustic\Assignment1\3" alt="image-20250202144154293" style="zoom: 50%;" />

- ##### Excitation Factoring

  <img src="D:\DT2212 Music Acoustic\Assignment1\4" alt="image-20250202144651050" style="zoom:80%;" />

  ​        Improve the efficiency of piano synthesis through "excitation factorization". Implementing the high-Q resonant sections of the soundboard and piano case separately as digital filters can simplify the impulse response and shorten the required excitation table length, thereby reducing memory requirements. These resonators can be implemented with parametric equalizer sections, one for each high-Q resonance. Figure 6 shows a possible resonator layout. Since the system is linear and time-invariant, the order of all elements can be arbitrary.

### 1.4 String Interface: Physical model of piano string and its implementation in digital synthesis

<img src="D:\DT2212 Music Acoustic\Assignment1\5" alt="image-20250202145659368" style="zoom: 67%;" />

The figure above shows the excitation process of a piano string, especially the physical position of the hammer hitting the string. In reality, the hammer hits the piano string between the two ends, far away from the hammer and the bridge. The figure uses a filter delay loop to show the implementation of this physical model.

The figure below shows the commutativity of linear, time-invariant systems, which further simplifies the structure. The entire structure can be regarded as a traditional filter delay loop. A second input (reverse signal) is added to the loop, which is added to a position in the loop to form the response of the string.

This process simulates the physical properties of the piano string through a delay loop and feedback mechanism, which can achieve accurate synthesis of the string excitation and vibration.

<img src="D:\DT2212 Music Acoustic\Assignment1\6" alt="image-20250202150135834" style="zoom:67%;" />

- Another application

  <img src="D:\DT2212 Music Acoustic\Assignment1\7" alt="image-20250202150655627" style="zoom: 67%;" />

  The figure above shows another application, where a second input is fed through a separate comb filter, separating the input signal from the string delay loop. The delay of the comb filter and feedback loop is the sum of the two delays in the previous model. The benefits of this are that (1) automatic loop calibration is simplified, and (2) the comb filter can be implemented elsewhere, such as in an effects unit.

  The figure below shows how comb filtering can be implemented using a second delay line "tap". The output of this new "tap" is added (or subtracted, depending on the loop implementation) to the output of the filter delay loop. By making the new "tap" a moving interpolation "tap" (e.g., using linear interpolation), a chorus effect can be achieved, or by adding multiple moving "tap" and adding/subtracting their outputs (with a selectable scaling factor), an economical chorus or Leslie effect can be provided.

  <img src="C:\Users\cheny\AppData\Roaming\Typora\typora-user-images\image-20250202150720653.png" alt="image-20250202150720653" style="zoom:67%;" />

### 1.5 Conclusion

An efficient computational model of the piano based on an acoustic model is described. The string-force interactions are modeled as discrete events, which can be modeled as continuous impulse responses of one or a few low-order digital filters. The soundboard and shell filtering are replaced with lookup tables, using one or a few read pointers per note.

### 2 Connection with the general theory

This paper on piano synthesis can be linked to the general theory presented in the course, especially in the <u>physical modeling</u> and <u>synthesis of string instruments</u>. The course literature generally emphasizes the vibration modes of the string, the resonance effects, and the interaction between the string and other structures (e.g., bridges, soundboards), all of which determine the <u>sonic characteristics of the instrument</u>. The piano synthesis models proposed in the paper (e.g., filter-delay loops, comb filters, excitation factorization, etc.) are consistent with these theories, especially when modeling the vibration and resonance characteristics of piano strings. The modeling approach adopted in the paper has a direct connection with the physical model of string instruments in the course.

For example, <u>the filter-delay loop and comb filter structures</u> mentioned in the paper are similar to the <u>physical model of the string</u>, in which the vibration of the string is <u>simulated by delays and feedback in the loop</u>, an approach that is consistent with the theory of string vibration and force propagation described in the course. With this modeling approach, the authors are able to effectively simulate multiple excitations of the string and complex string-hammer interactions, while achieving resonance phenomena through comb filters, thereby reproducing the richness of the piano timbre.

In addition, the resonance of strings mentioned in the paper (especially the <u>resonance of the soundboard and the piano case</u>) is closely related to the discussion of the propagation and resonance of musical instruments in the course. The course emphasizes how to process the harmonic response of musical instruments through models and how to enhance the realism of synthesis by accurately simulating the vibration of the resonant body. The paper reflects the application of this theory by abstracting the resonance effect from the actual structure and using digital filters to process it.

Therefore, the piano synthesis method used in this paper is closely related to the theory in the "Music Acoustics" course. It successfully realizes efficient and low-computational cost piano sound synthesis by simulating the physical properties of strings and resonators.

### 3 Potential problems

- ##### Physical simulation:

  The study simplified the hammer-string interaction into <u>several discrete impact pulses</u>, and <u>only set the velocity</u> as the input variable. Although this is more efficient in computation, it may not fully capture the complex nonlinear interaction between the string and the hammer. In fact, the interaction between the hammer and the string is continuous, involving dynamic changes in the <u>hammer's velocity, pressure, etc</u>. This simplification may cause distortion of some details, especially in the simulation of strong blows or nonlinear behavior.

- ##### Model limitations of string-resonator interaction:

  The high Q characteristics of the resonator are treated independently in the model, which may <u>ignore the more complex coupling effects</u> between the string and the soundboard, which may <u>affect the accuracy and richness</u> of the timbre.

### 4 Suggested ideas

May be try to simulate the changes in pressure and energy dissipation during each hammering process, taking into account the influence of the string's stiffness changing with the vibration state. In order to more accurately simulate the nonlinear coupling between the string and the soundboard, and capture the resonance effects from other strings, thereby achieving more realistic and dynamic sound synthesis.