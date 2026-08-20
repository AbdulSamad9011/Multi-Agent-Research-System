# MRI Brain Tumor Detection Using Deep Learning and Machine Learning Approaches

**Journal:** *Measurement: Sensors* 31 (2024) 101026  
**Available online:** 7 January 2024  
**Authors:** Shenbagarajan Anantharajan$^{a,*}$, Shenbagalakshmi Gunasekaran$^a$, Thavasi Subramanian$^a$, Venkatesh R$^b$  
$^a$ *Mepco Schlenk Engineering College, Sivakasi - 626005, Virudhunagar, Tamilnadu, India*  
$^b$ *Ramco Institute of Technology, Rajapalayam - 626117, Virudhunagar, Tamilnadu, India*  

---

## Article Info
* **Keywords:** 
  * Brain tumour
  * Magnetic resonance imaging (MRI)
  * Deep learning (DL)
  * Machine learning (ML)
  * Adaptive contrast enhancement algorithm (ACEA)
  * Gray-level co-occurrence matrix (GLCM)
  * Ensemble deep neural support vector machine (EDN-SVM)

---

## Abstract
The development of aberrant brain cells, some of which may become cancerous, is known as a brain tumour. The quality of life and life expectancy of patients are enhanced by early and timely illness identification and treatment plans. Magnetic Resonance Imaging (MRI) scans are the most common approach for finding brain tumors. However, the ability of radiologists and other clinical experts to identify, segment, and remove contaminated tumour regions from MRI images is a critical factor in a process that is iterative and labor-intensive and relies on those individuals’ abilities in these areas. Concepts for image processing may envision the diverse human organ anatomical structures. It is difficult to find abnormal brain regions using simple imaging methods. Over the last several years, interest in the emerging machine learning field of “Deep Learning (DL)” has grown significantly. It was extensively used in numerous applications and shown to be an effective Machine Learning (ML) technique for many of the challenging issues. 

This research suggests a novel MRI brain tumour detection method based on DL and ML. Initially, the MRI images are collected and preprocessed using Adaptive Contrast Enhancement Algorithm (ACEA) and median filter. Fuzzy c-means based segmentation is done to segment the preprocessed images. The features like energy, mean, entropy, and contrast are extracted using Gray-level co-occurrence matrix (GLCM). The abnormal tissues are classified using the proposed Ensemble Deep Neural Support Vector Machine (EDN-SVM) classifier. The numerical findings reveal a better accuracy (97.93%), sensitivity (92%), and specificity (98%) in recognizing aberrant and normal tissue from brain MRI images, which supports the effectiveness of the approach that was recommended.

---

## 1. Introduction

The human brain is regarded to be one of the most essential organs since it is responsible for a large number of the body’s regulatory processes, including memory, emotions, vision, motor skills, responses, and breathing. In the event that a tumour begins to form inside the brain, these functions will be significantly disrupted [1,3]. This tumour is either a primary brain tumour (BT), which develops from inside the brain itself and represents the development of brain tissues themselves, or it is a metastatic BT, which develops in another part of the body and eventually spreads to the brain. 

When compared to tumors that originate in any other organ of the human body, those that occur in the brain provide a significant diagnostic challenge. Because the brain has the “Blood-Brain Barrier (BBB)”, ordinary radioactive markers are unable to detect the hyperactivity of tumour cells in the body [2]. Consequently, MRI scans are considered to be the most effective diagnostic tracers for detecting breaches in the BBB.

There are between 7 and 11 cases of brain tumors per 100,000 people in various age groups per year. It is estimated that 227,000 people die each year as a result of this dreadful illness. In addition, about 7.7 million survivors are adjusting to life with a disability [4]. As well as saving lives, an early diagnosis of a brain tumour may help prevent disability. The brain, the body’s most delicate organ, will be subjected to less modification and surgery if it is detected early. To begin with, a radiologist will need to take a picture of the affected area in order to do a manual diagnosis [5]. After that, an experienced physician is consulted for the purpose of image analysis and the formulation of a treatment strategy. Unfortunately, the research that investigated the accuracy of manually diagnosing brain tumors reported a discrepancy amongst the experts who reviewed the data. According to reports, the level of agreement amongst specialists for the manual diagnosis of a BT is between 90 and 95%. The degree of disagreement amongst the specialists is further reduced when it comes to mixed types of tumour, mixed glioma, and medulloblastoma, falling to 77% and 58%, respectively [6].

Digital image processing and other advancements in medical imaging have contributed to the widespread use of computer-aided diagnosis (CAD) in recent years. The MRI technique is favoured for use in diagnostic systems like these since it does not pose a threat from ionising radiation and is able to reliably identify blood flow in veins [7]. The use of large medical image datasets, such as Brain MRI scans, for the identification of BT may be aided by the use of ML and DL algorithms. Creating a ML and DL model is a multistep process that involves training using a significant quantity of medical imaging data [8]. This is necessary in order to get the correct prediction or insight from the model, which is necessary in order to make an appropriate clinical decision. In this study, we investigate the identification of brain tumors using DL and ML techniques.

### Major Contributions:
- To preprocess the MRI images, Adaptive Contrast Enhancement Algorithm (ACEA) and median filter is used.
- Fuzzy c-means based segmentation is done to segment the preprocessed images.
- The features are extracted using GLCM approach.
- The abnormal tissues are classified using the proposed EDN-SVM classifier.

---

## 2. Related Works

The author of [9] suggested method identifies the kind of tumors present in the BT MRI image and marks the tumour region. AlexNet model and the Faster R–CNN algorithm’s Region Proposal Network (RPN) are utilised as the basic models for classifying various tumour kinds. The study [10] employed a Deep NN classifier, a component of the deep learning designs, to divide 66 brain MRI scans into four categories, including “normal”, “glioblastoma”, “sarcoma”, and “metastatic bronchogenic carcinoma tumors”. The author of [11] constructed brain MRI images were utilised to create a Convolutional Neural Network (CNN) to identify a tumour. In Ref. [12], the author used a CNN-based methodology as well as a deep neural network technique to categorise an MRI as “tumour detected” or “tumour not detected.” The study [13] showed the promise of DL in MRI scans as a non-invasive method for simultaneous and automated tumors segmentation, identification, and grading of LGG in clinical settings. The research [14] presents a faster and more accurate method for detecting human brain cancers by combining the “Template-based K-means (TK)” algorithm with pixels in the image and “Principal Components Analysis (PCA)”.

The “Watershed Dynamic Angle Projection - Convolution Neural Network (WDAPP-CNN)” is able as a nation method for tumors identification in this research [15]. The tumors area was successfully segmented using the watershed technique. The research [16] suggested technique guarantees to be very effective and exact for detecting, classifying, and segmenting brain tumors. Automated segmentation is performed on image data using a CNN-based method, which employs very small kernel sizes of 3×3. The author of [17] focused early identification of benign brain tumors. Segmentation is required in the early stages of brain tumors identification. Algorithms usually for segmentation have several limitations, including the inability to handle noisy data and the inability to identify subtle intensity variations in the image. The study of [18] presented a comprehensive and entirely automated MRI brain tumors identification and segmentation approach employing the “Gaussian mixture model”, “Fuzzy C-Means”, “active contour”, “wavelet transform”, and “entropy segmentation” techniques as an effective clinical-aided tool. The two key components of the suggested approach are tumors auto-detection and segmentation as well as skull removal.

The research [19] suggested approach tries to distinguish between BT and normal brains. Brain magnetic resonance imaging is used to research various forms of brain malignancies. Support vector machines and various wavelet transformations are used to identify and categorise MRI brain cancers. The Study [20] proposed hybrid K-means Galactic Swarm Optimization (GSO) technique is adopted as a practical solution to the image segmentation issue, which is considered as a classification model. Study developed a Fuzzy C-Means clustering technique, which was followed by conventional detectors and CNN to remove brain tumors from 2D MRI. The experiment utilised real-time dataset with various tumors sizes, locations, forms, and image brightness. The author of [21] presented a comprehensive assessment of the literature on current approaches to segmenting BT from brain MRI data. The author of [26] provided a thorough critique of the research and discoveries made in the recent past to identify and categorise brain tumors using MRI scans. According to the study [27] an automated approach is offered to distinguish between malignant and non-cancerous brain MRI scans. Using three benchmark datasets, the suggested technique is verified, with average results of 97.1% accuracy, 0.98 area under the curve, 91.9% sensitivity, and 98.0% specificity. The study [28] proposes a two-step Dragonfly algorithm (DA) clustering method to precisely extract starting contour points.

### 2.1. Problem Statement
Brain tumors have the potential to generate consequences such as physical impairments, which would then need patients to undergo very intensive therapy, which is often rather painful, in order to cure or lessen the caused disabilities. In addition, the negative effects that brain tumors have on the functioning of the brain might vary depending on the size of the tumour, where it is located, and what kind it is. Because a tumour might exert pressure on the region of the brain that regulates the body's mobility, the patient can become immobile as a result of this. If it is diagnosed sooner, it may be possible to prevent disability from occurring. There are a number of obstacles that need to be overcome in order to correctly categorise brain tumors, including high variation regarding size, shape, and intensity across different pathological types.

---

## 3. Proposed Methodology

This section provides a comprehensive discussion of the identification of MRI brain tumors utilizing both DL and ML techniques. In the beginning, MRI brain tumour data were obtained and preprocessed with the help of ACEA and the median filter in order to get rid of the noise. In order to segment the MRI brain images, a fuzzy c-means technique is applied, and a GLCM matrix is used to extract the features of the images. The EDN-SVM approach is then used to classify the images of healthy and tumorous brain tissue.

### 3.1. Dataset Collection
We utilize a dataset that may be found on the Kaggle open data website in order to evaluate the performance of the suggested architectural design. This dataset includes 255 T1-mode MRI images. It includes 98 MRI slices taken from healthy brain tissue and 155 MRI slices taken from tumorous brain tissue. Because each of these images had a unique dimension, we resized the images such that their width and height are the same before moving on to the preprocessing stage.

### 3.2. Preprocessing

#### 3.2.1. Adaptive Contrast Enhancement Algorithm (ACEA)
MRI image contrast is crucial for tumour identification since this technique relies heavily on image brightness. Here, we use an automated and dynamic method to extract the parameters from each image. A brain tumour ($T$), healthy brain tissue ($B$), and vessels ($V$) can all be distinguished in an MRI image dataset.

In addition to averaging their values ($\mu_T^Z, \mu_B^Z, \mu_V^Z$), and calculating their standard deviations ($\sigma_T, \sigma_B, \sigma_V$), we additionally calculate the highest PDF intensity value for the brain class, $N^Z$. The mean value has the $\mu_T^Z < \mu_B^Z < \mu_V^Z$ characteristic.

Set the lower limit as $P_{\min} = \mu_T - 3\sigma_T$ and the upper limit as $P_{\max} = \mu_V + 3\sigma_V$. The formula for intensity transform of range 0–255 is:

$$I_{out} = egin{cases} 0 & 	ext{if } I_x < P_{\min} 	ext{ or } I_x > P_{\max} \ rac{I_x - P_{\min}}{P_{\max} - P_{\min}} 	imes 255 & 	ext{if } P_{\min} \le I_x \le P_{\max} \end{cases}$$

#### 3.2.2. Median Filter
When applied to MRI scans of the brain, this nonlinear technique effectively eliminates unwanted background noise while preserving edges. Salt and pepper noise may be eliminated with great success.

$$c(i, j) = 	ext{median}_{(a, b) \in G_{ij}} \{ k(a, b) \}$$

where $G_{ij}$ denotes the sets of coordinates centred on $(i, j)$ within the window frame.

### 3.3. Fuzzy C-Means (FCM) Segmentation
The FCM method seeks to achieve the lowest possible value for the objective function shown below:

$$Y(O, f_1, f_2, \dots, f_c) = \sum_{x=1}^c \sum_{y=1}^m o_{xy}^n s_{xy}^2$$

where $s_{xy}$ is the Euclidean distance between the $x$-th centroid and $y$-th data point, $n \in [1, \infty)$ is a weighting exponent, and $o_{xy}$ is the degree of membership.

$$o_{xy} = rac{1}{\sum_{k=1}^c \left( rac{s_{xy}}{s_{ky}} ight)^{rac{2}{n-1}}}$$

$$f_x = rac{\sum_{y=1}^m o_{xy}^n i_y}{\sum_{y=1}^m o_{xy}^n}$$

The iteration ends when $\max_{xy} \{ |o_{xy}^{(g+1)} - o_{xy}^{(g)}| \} < \epsilon$.

### 3.4. Feature Extraction using GLCM
Gray-Level Co-occurrence Matrix (GLCM) extracts second-order statistical textural qualities:

- **Entropy:** 
  $$	ext{Entropy} = -\sum_{x=0}^{N-1} \sum_{y=0}^{N-1} T_{xy} \log T_{xy}$$
- **Correlation:** 
  $$	ext{Correlation} = rac{\sum_{x=0}^{N-1} \sum_{y=0}^{N-1} (x - \mu_x)(y - \mu_y) T(x, y)}{\sigma_x \sigma_y}$$
- **Energy:** 
  $$	ext{Energy} = \sum_{x=0}^{N-1} \sum_{y=0}^{N-1} T_{xy}^2$$
- **Contrast:** 
  $$	ext{Contrast} = \sum_{m=0}^{N-1} m^2 \sum_{x=0}^{N-1} \sum_{y=0}^{N-1} T(x, y)$$
- **Mean:** 
  $$\mu = \sum_{x=0}^{N-1} x \cdot T(x)$$
- **Standard Deviation & Variance ($\sigma^2$):** 
  $$\sigma^2 = \sum_{x=0}^{N-1} (x - \mu)^2 T(x)$$

### 3.5. Classification using Ensemble Deep Neural Support Vector Machine (EDN-SVM)
The proposed EDN-SVM estimator architecture consists of four primary parts:
1. An input layer with $S$ nodes.
2. A central feature layer with $s$ nodes.
3. A set of $s$ two-layer Neural Networks (MLPs), each taking the input layer and producing one attribute value.
4. A primary Support Vector Regression model $N$ that takes the entire feature layer as input to compute output.

#### Training Algorithm Summary:
```
Algorithm 1: EDN-SVM
---------------------------------------------
1. Initialize main SVM N
2. Initialize NNs
3. repeat:
    a. Calculate kernel matrix for main SVM N
    b. Train main SVM N
    c. Use backpropagation on the dual objective of N to train the NNs
4. until stop condition (maximal number of epochs)
```

---

## 4. Results and Discussion

Implementation was performed in Python 3.7.16. Performance was compared against CNN, Random Forest Classifier (RFC), Artificial Neural Network (ANN), and Region-based CNN (R-CNN).

### Summary Performance Comparison Table

| Method / Model | Accuracy (%) | Computational Time (min) | PSNR (dB) | Sensitivity (%) | Specificity (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **CNN [22]** | 88.5 | 3.0 | 44.5 | 68.0 | 72.0 |
| **RFC [23]** | 91.2 | 6.0 | 45.1 | 72.5 | 78.0 |
| **ANN [24]** | 89.8 | 8.0 | 46.2 | 75.0 | 81.0 |
| **R-CNN [25]** | 93.5 | 4.0 | 40.3 | 82.0 | 88.0 |
| **EDN-SVM (Proposed)** | **97.93** | **2.0** | **52.98** | **92.0** | **98.0** |

### Evaluation Formulas:
- **Accuracy:** 
  $$	ext{Accuracy} = rac{TP + TN}{TP + TN + FP + FN} 	imes 100$$
- **Sensitivity:** 
  $$	ext{Sensitivity} = rac{TP}{TP + FN} 	imes 100$$
- **Specificity:** 
  $$	ext{Specificity} = rac{TN}{TN + FP} 	imes 100$$
- **PSNR:** 
  $$	ext{PSNR} = 10 \log_{10} \left( rac{255^2}{	ext{MSE}} ight)$$
- **Jaccard Coefficient:** 
  $$	ext{JC} = rac{|A \cap B|}{|A \cup B|}$$

---

## 5. Conclusion

The suggested EDN-SVM method proposes a novel method of image classification achieving **97.93% accuracy**, **92% sensitivity**, and **98% specificity** in detecting brain tumors from MRI scans. Future directions include embedding the algorithm in clinical software and extending the framework to 3D brain MRI scans and color images.

---

## References

1. E. Schulz, S.J. Gershman, The algorithmic architecture of exploration in the human brain, *Curr. Opin. Neurobiol.* 55 (2019) 7-14.
2. P.J. van Lonkhuizen, et al., Interventions for cognitive problems in adults with brain cancer, a narrative review, *Eur. J. Cancer Care* 28 (3) (2019) e13088.
3. A. Del Dosso, et al., Upgrading the physiological relevance of human brain organoids, *Neuron* 107 (6) (2020) 1014-1028.
4. S.L. Fernandes, et al., A reliable framework for accurate brain image examination and treatment planning based on early diagnosis support for clinicians, *Neural Comput. Appl.* 32 (20) (2020) 15897-15908.
5. Z.U. Rehman, et al., Fully automated multi-parametric brain tumour segmentation using superpixel based classification, *Expert Syst. Appl.* 118 (2019) 598-613.
6. Z.U. Rehman, et al., Texture based localization of a brain tumor from MR-images by using a machine learning approach, *Med. Hypotheses* 141 (2020) 109705.
7. C. KV, G.G. King, Brain tumour classification: a comprehensive systematic review on various constraints, *Imaging & Visualization*, 2022, pp. 1-13.
8. K. Rezaei, et al., Multi-objective differential evolution-based ensemble method for brain tumour diagnosis, *IET Image Process.* 13 (9) (2019) 1421-1430.
9. R. Ezhilarasi, P. Varalakshmi, Tumor detection in the brain using faster R-CNN, *2nd International Conference on I-SMAC*, IEEE, 2018, pp. 388-392.
10. H. Mohsen, et al., Classification using deep learning neural networks for brain tumors, *Future Computing and Informatics Journal* 3 (1) (2018) 68-71.
11. M. Siar, M. Teshnehlab, Brain tumor detection using deep neural network and machine learning algorithm, *ICCKE*, IEEE, 2019, pp. 363-368.
12. C.L. Choudhury, et al., Brain tumor detection and classification using convolutional neural network and deep neural network, *ICCSEA*, IEEE, 2020, pp. 1-4.
13. M.A. Naser, M.J. Deen, Brain tumor segmentation and grading of lower-grade glioma using deep learning in MRI images, *Comput. Biol. Med.* 121 (2020) 103758.
14. M.K. Islam, et al., Brain tumor detection in MR image using superpixels, principal component analysis and template based K-means clustering algorithm, *Machine Learning with Applications* 5 (2021) 100044.
15. T.A. Jemimma, Y.J. Vetharaj, Watershed algorithm based DAPP features for brain tumor segmentation and classification, *ICSSIT*, IEEE, 2018, pp. 155-158.
16. G. Hemanth, et al., Design and implementing brain tumor detection using machine learning approach, *ICOEI*, IEEE, 2019, pp. 1289-1294.
17. S.K. Chandra, M.K. Bajpai, Effective algorithm for benign brain tumor detection using fractional calculus, *TENCON 2018*, IEEE, 2018, pp. 2408-2413.
18. M. Gurbina, et al., Tumor detection and classification of MRI brain image using different wavelet transforms and support vector machines, *TSP*, IEEE, 2019, pp. 505-508.
19. C. Sheela, G. Suganthi, Brain tumor segmentation with radius contraction and expansion based initial contour detection for active contour model, *Multimed. Tools Appl.* 79 (33) (2020) 23793-23819.
20. S.J. Nanda, et al., A K-means-galactic swarm optimization-based clustering algorithm with Otsu's entropy for brain tumor detection, *Appl. Artif. Intell.* 33 (2) (2019) 152-170.
21. A. Wadhwa, et al., A review on brain tumor segmentation of MRI images, *Magn. Reson. Imaging* 61 (2019) 247-259.
22. M.L. Martini, E.K. Oermann, Intraoperative brain tumour identification with deep learning, *Nat. Rev. Clin. Oncol.* 17 (4) (2020) 200-201.
23. M. Soltaninejad, et al., Supervised learning based multimodal MRI brain tumour segmentation using texture features from supervoxels, *Comput. Methods Programs Biomed.* 157 (2018) 69-84.
24. N. Arunkumar, et al., Fully automatic model-based segmentation and classification approach for MRI brain tumor using artificial neural networks, *Concurrency Comput. Pract. Ex.* 32 (1) (2020) e4962.
25. K. Salçin, Detection and classification of brain tumours from MRI images using faster R-CNN, *Tehnicki glasnik* 13 (4) (2019) 337-342.
26. M. Nazir, et al., Role of deep learning in brain tumor detection and classification (2015 to 2020): a review, *Comput. Med. Imaging Graph.* 91 (2021) 101940.
27. J. Amin, et al., A distinctive approach in brain tumor detection and classification using MRI, *Pattern Recogn. Lett.* 139 (2020) 118-127.
28. H.A. Khalil, et al., 3D-MRI brain tumor detection model using modified version of level set segmentation based on dragonfly algorithm, *Symmetry* 12 (8) (2020) 1256.
