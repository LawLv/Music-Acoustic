# Assignment 4

Yilai Chen

###### I choose questions 2 and 4. (Question 1 is a backup if it can be reviewed)

## Q2

Source: Lecture 7 Synthesis methods and sampling, `Synthmethods VT23.pdf`

**a)** In wavetable synthesis, each waveform is typically recorded at a fixed dynamic level. To achieve a continuous change of dynamics within a sustained note, there are two methods:

- Record Multiple Samples and Interpolate:

  Record the same note at various dynamic levels (soft, medium, loud). Use a smooth crossfade or interpolation between these pre‐recorded wavetables based on real-time performance parameters (such as key velocity). This method allows the timbre and intensity to vary continuously as the player modulates dynamics.

- Phase-Adjusted Single-Period Sampling:

  We can sample a single period of the waveform under several pitch/dynamic conditions, perform a Fourier transform with phase alignment, and then use the inverse transform to obtain a waveform that can be interpolated. This “parameter smoothing” technique enables gradual transitions in dynamics while preserving harmonic structure.

**b)** Wavetable synthesis relies on fixed, pre-recorded samples at specific pitches.

- Fixed Harmonic Structure:

  Each wavetable is recorded at one particular pitch with its harmonics aligned to that frequency. Attempting to change pitch by simply speeding up or slowing down the sample will alter the harmonic relationships, causing the timbre to distort.

- “Parrot Effect”:

  The sample always sounds like the original recording. Changing the playback speed to create a glide introduces unwanted artifacts (such as aliasing and unnatural spectral shifts) and this will fail to capture the subtle interactions found in a real instrument’s pitch control.

**c)** Use “physical modelling”.

- Air Column Modeling:

  The clarinet’s body (air column) can be modeled as a delay line. The length of this delay line determines the pitch. By continuously varying the delay (the effective length of the air column) to achieve smooth pitch glides.

- Reed Simulation:

  The clarinet’s reed is modeled as a nonlinear element that interacts with the air column. A nonlinear function simulates the reed’s behavior in response to changes in breath pressure and lip tension.

- Feedback Loop and Filtering:

  The system is arranged in a feedback loop where the reed’s output is sent through the delay line and then filtered to account for frequency-dependent losses and resonances. 

Adjusting the delay line’s length enables smooth pitch glides without distorting the harmonic structure, while variations in excitation (via the reed model) produce natural dynamic changes.

- **Limitations**:

  This is a complex system that requires a lot of detail to build and model, and it is also very demanding on the computer. It also takes a lot of time to adjust the parameters to achieve the effect of the clarinet. 

## Q4

Source: Lecture 6 Guitar and Piano, `[Lecture06-1.pdf]`

**a)** For a justly tuned major third above A4, the frequency ratio is 5 ⁄ 4. With A4 = 440 Hz, the just major third is 550 Hz.
In equal temperament, a major third is 4 semitones above A4 with a ratio of 2 ^ (4 ⁄ 12) ≈ 1.25992, so 440 × 1.25992 ≈ 554.37 Hz
Thus, the just major third is lower than the equal‐temperament note. In cents the deviation is
$$
\Delta\,(\text{cents}) = 1200 \cdot \log_{2}\!\left(\frac{5/4}{2^{4/12}}\right)\\
= 1200 \cdot \log_{2}\!\left(\frac{1.25}{1.25992}\right)\\
\approx 1200 \cdot \log_{2}(0.99213)\\
\approx 1200 \times (-0.01140) \approx -13.68\,\text{cents}.
$$

So a normal tuner should display approximately –14 cents for the major third (i.e. 13.7 cents flat relative to equal temperament).

**b)** When considering the effect of inharmonicity, the frequency of the nth partial of an ideal piano string is given by
$$
f_n = nf_1 \sqrt{1 + B\,n^2},\\
with B = 6 \times 10^{-4}.
$$
In ideal (harmonic) theory the lowest partial pair that would coincide between the A4 string and the major-third string are:

For the A4 string (f₁ = 440 Hz), the 5th partial(ideally):  
$$
5\times440 = 2200Hz
$$
For the major third string (f₁ = 550 Hz in just intonation), the 4th partial(ideally): 
$$
4\times550 = 2200Hz
$$
Now, applying inharmonicity:

A4 String (5th partial):
$$
f_{A,5} = 5 \times 440 \sqrt{1 + 6 \times 10^{-4} \times 5^2}\\
= 2200 \sqrt{1 + 0.015} = 2200 \sqrt{1.015} \approx 2200 \times 1.00746 \approx 2216.4\,\text{Hz}.
$$
Major Third String (4th partial):
$$
f_{T,4} = 4 \times 550 \sqrt{1 + 6 \times 10^{-4} \times 4^2}\\
= 2200 \sqrt{1 + 0.0096} = 2200 \sqrt{1.0096} \approx 2200 \times 1.00479 \approx 2210.5\,\text{Hz}.
$$
The cent deviation between these two partials is
$$
\Delta\,(\text{cents}) = 1200 \cdot \log_{2}\!\left(\frac{2216.4}{2210.5}\right).
$$
Calculating the ratio: 
$$
\frac{2216.4}{2210.5} \approx 1.00267,
$$
Then, 
$$
log_{2}(1.00267) \approx \frac{\ln(1.00267)}{\ln 2} \approx \frac{0.00267}{0.6932} \approx 0.00385,\\
So, \Delta\,(\text{cents}) \approx 1200 \times 0.00385 \approx 4.62\,\text{cents}.
$$
The difference in frequency is
$$
2216.4\,\text{Hz} - 2210.5\,\text{Hz} \approx 5.9\,\text{Hz}.
$$
which is the beating frequency between these partials.

**c)** Perceived Roughness and Sources: A beating frequency of  5.9 Hz difference.

The inharmonicity inherent in piano strings (B = 6×10⁻⁴) causes all partials to deviate slightly from ideal integer multiples. Even when the fundamental intervals are tuned to just intonation, these deviations mean that many partials will not align perfectly across strings. Also, higher partials with smaller frequency differences may produce faster beats that contribute to a sensation of roughness or dissonance. Further more, slight variations between different strings and interactions with the soundboard can lead to additional detunings that leading to the overall roughness.



## Q1 

Source: Lecture 2 Modes of vibration, Percussion P5-8, 52

**a)** 
$$
First \; tone: f_0 \approx 110Hz, \\
partial \; tones \; are \; at \; 240 Hz, \;370 Hz, \;504 Hz, \;636Hz \\
Second \; tone: f_0 \approx 142Hz, \\
partial \; tones \; are \; at \; 313 Hz, \;476 Hz, \;652 Hz, \;816Hz\\
First \; tone: f_0 \approx 206Hz, \\
partial \; tones \; are \; at \; 444 Hz, \;652 Hz, \;909 Hz, \;1149Hz
$$
From these data, it can be seen that the subsequent partials of each tone are not integer multiples of the fundamental frequency, indicating that they are not "pure harmonic" structures, but are inharmonicity.

**b)** It may be the glockenspiel and marimba because they have larger amplitudes of non-integer multiple partial tones. Instruments with metal or bell-shaped resonators (such as bells and glockenspiels) are more consistent with these frequency relationships than orchestral instruments.

**c)** 
$$
First \;note \approx 110\,\text{Hz} \rightarrow A_2 (MIDI \;45)\\
Second \;note \approx 142\,\text{Hz} \rightarrow C\#3 (MIDI \;49)\\
Third \;note \approx 206\,\text{Hz} \rightarrow G\#3 (MIDI \;56)
$$


Hence, the three notes are A2, C\#3, and G\#3 in standard tuning.









