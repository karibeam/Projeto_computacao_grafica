# Feature Specification: Refactor Rendering Pipeline Steps

**Created**: 2026-04-14
**Status**: Draft

## User Scenarios & Testing

### Primary User Flow
As a computer graphics student/instructor, I want to see progressive rendering concepts demonstrated clearly across different steps so that I can understand how each technique improves image quality.

### Scenario 1: Step 3 Comparison
- **Given** I am rendering step 3 with antialiasing
- **When** I execute step 3
- **Then** two images are generated: one with single point light and another with two point lights (like current step 4.1)

### Scenario 2: Step 4 Simplification  
- **Given** I am rendering step 4
- **When** I execute step 4
- **Then** only the sphere is rendered with antialiasing, Phong illumination, and a single point light (no step 4.1)

### Scenario 3: Step 5 Area Light Sampling
- **Given** I am rendering step 5
- **When** I execute step 5  
- **Then** the scene uses area light with 32 uniform samples per pixel for soft shadows and penumbra effects

## Functional Requirements

### FR1: Step 3 Dual Output
The system shall generate two separate images for step 3:
- **FR1.1**: First image (`step_3_single_light.png`) with single point light configuration
- **FR1.2**: Second image (`step_3_dual_light.png`) with two point lights (left and right side)
- **FR1.3**: Both images use antialiasing (multiple rays per pixel)
- **FR1.4**: Both images use Phong illumination model with shadows

### FR2: Step 4 Simplification
The system shall simplify step 4 to demonstrate basic antialiasing with single light:
- **FR2.1**: Step 4 renders sphere only with antialiasing
- **FR2.2**: Uses Phong illumination model with single point light
- **FR2.3**: Step 4.1 is removed entirely from the pipeline
- **FR2.4**: Output file: `step_4.png`

### FR3: Step 5 Area Light with Uniform Sampling
The system shall implement advanced area light sampling in step 5:
- **FR3.1**: Step 5 uses area light source instead of point light
- **FR3.2**: Each pixel ray calculates 32 uniformly distributed samples across the area light surface
- **FR3.3**: Soft shadows and penumbra effects are visible
- **FR3.4**: Uses ellipsoid geometry (incremental from step 4)
- **FR3.5**: Output file: `step_5.png`

### FR4: Pipeline Execution Order
The rendering pipeline shall execute steps in order: 1, 2, 3 (dual output), 4, 5
- **FR4.1**: No step 4.1 exists in the new pipeline
- **FR4.2**: Step 3 produces two output files
- **FR4.3**: Total output files: 6 (step_1.png, step_2.png, step_3_single_light.png, step_3_dual_light.png, step_4.png, step_5.png)

## Success Criteria

- **SC1**: Step 3 generates exactly 2 images with different lighting configurations
- **SC2**: Step 4 renders in under 30 seconds with single point light and antialiasing  
- **SC3**: Step 5 shows visible soft shadows with 32 area light samples per pixel
- **SC4**: All pipeline steps execute without errors in sequential mode
- **SC5**: Total pipeline execution produces 6 output files

## Key Entities

### Scene Configuration
- Camera position and orientation
- Light sources (point lights, area lights)
- Geometric objects (sphere, ellipsoid, plane)
- Material properties (Phong parameters)

### Rendering Parameters  
- Rays per pixel (antialiasing)
- Light samples (area light sampling)
- Random seed for reproducibility

### Output Artifacts
- PNG image files for each step
- Execution time metrics

## Assumptions

- Existing rendering engine (ray tracer) supports both point and area lights
- Phong illumination model is already implemented
- Antialiasing via supersampling is functional
- Area light sampling infrastructure exists
- File output system handles PNG generation
