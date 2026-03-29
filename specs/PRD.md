# PRD (Product Requirements Document)
## 1. Users & Value（Users & Value）
The core users of this product are music enthusiasts, beginner composers, and small music studios. This product uses transformer-based generative AI to quickly generate music scores that meet users' needs, lowering the threshold for composition and saving creation time. It can help users overcome creative bottlenecks, providing a wealth of musical inspiration for those who lack professional composition skills. In addition, it can improve the efficiency of small music studios in creating background music and demo scores.

## 2. Scope & Non-Goals（Scope & Non-Goals）
The scope includes generating complete and playable music scores based on the style, tonality, and instrument type input by users. It supports adjusting the tempo and rhythm of the generated scores to meet different user preferences. It does not include post-editing of complex scores, instrument recording functions, nor does it support professional-level score printing and typesetting. These advanced functions are beyond the current project scope and will not be developed temporarily.

## 3. KPIs & Constraints（KPIs & Constraints）
The KPI goals are that the music score generation success rate is ≥90%, the generation time is ≤10 seconds per piece, and the user satisfaction is ≥80%. The success rate is defined as the proportion of scores that are logically coherent and playable without obvious errors. The constraints are that a single generated score does not exceed 50 bars, and it supports score generation for common instruments (piano, guitar, violin). It does not support rare instruments or overly complex polyphonic scores for the time being.

## 4. Risk Framing（Risk Framing）
The main risks are copyright disputes in the generated scores and high melody repetition. The generated melodies may inadvertently resemble existing copyrighted works, leading to legal risks. To mitigate these risks, a copyright filtering mechanism will be introduced to compare generated scores with existing copyrighted works. At the same time, the model training data will be optimized to increase the diversity of training samples, and special personnel will be arranged to review the generated content to reduce the risks of infringement and homogenization.

## 5. Sign-off（Sign-off）
The reviewers are the course teacher and the project leader. Through the GitHub CODEOWNERS and PR review mechanisms, it is ensured that the content of the PRD meets the course requirements and the project's actual needs. Only after the review is passed can the subsequent development work be carried out, ensuring that the project proceeds in accordance with the established requirements and avoiding deviations from the goal.
