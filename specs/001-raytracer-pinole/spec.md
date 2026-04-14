# Feature Specification: Progressive Pinhole Ray Tracer

**Feature Branch**: `001-raytracer-pinole`
**Created**: 2026-04-09
**Status**: Draft
**Input**: User description: "Crie uma aplicação em python de renderizacao de um cenário com um plano e uma esfera, utilizando câmera pinhole, o filme tem tamanho de 512x512 pixels, a aplicação deve renderizar o cenário de algumas diferentes, em passos, assim, a primeira renderização tera somente uma iluminação pontual e nenhum material na esfera somente a cor vermelha e a interação com a luz sem calculo de sombra. O próximo passo é renderização uma nova imagem com sombra, com o modelo de phong, verifique que é incremental cada etapa adiciona algo ou melhora a anterior, assim na proxima adiciona antialiasing, na próxima luz espacial, na proxima luz espacial com amostra uniforme, faca todos os calculos nas coordenadas locais para depois transformar para coordenadas globais por ultimo faca a renderização de uma elipse, quero passar as quantidades de amostras de raios pelo terminal, tanto os raios do filme quanto os raios da fonte de luz, quero poder escolher quantos raios por pixel."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Render Basic Scene with Point Light (Priority: P1)

The user runs the application to render a scene containing a plane and a sphere using a pinhole camera model. The initial rendering uses a single point light source with a red-colored sphere (no material model) and no shadow calculations. The output is a 512x512 pixel image.

**Why this priority**: This is the foundational rendering step that establishes the core ray tracing pipeline (camera, scene geometry, basic lighting). All subsequent steps build upon this.

**Independent Test**: Can be fully tested by running the application with default parameters and verifying the output image displays a red sphere on a plane with point light illumination and no shadows.

**Acceptance Scenarios**:

1. **Given** a scene with a plane and sphere, **When** the user runs the application with step 1 parameters, **Then** a 512x512 pixel image is generated showing a red sphere with point light illumination and no shadows
2. **Given** the camera uses a pinhole model, **When** rays are cast through each pixel, **Then** the intersection calculations are performed in local coordinates and transformed to global coordinates

---

### User Story 2 - Render with Shadows and Phong Model (Priority: P2)

The user runs the application to render the scene with shadow calculations enabled and the Phong illumination model applied to the sphere surface. This step builds on the basic rendering by adding realistic lighting and shadow effects.

**Why this priority**: Adds visual realism through shadows and the Phong reflection model, which are fundamental to computer graphics rendering.

**Independent Test**: Can be fully tested by running the application with step 2 parameters and verifying the output image shows shadows cast by the sphere and Phong shading on the sphere surface.

**Acceptance Scenarios**:

1. **Given** the scene from step 1, **When** the user enables shadows and Phong model, **Then** the rendered image shows shadows cast by objects and Phong illumination on the sphere
2. **Given** Phong model is active, **When** light interacts with the sphere surface, **Then** ambient, diffuse, and specular components are calculated

---

### User Story 3 - Render with Antialiasing (Priority: P3)

The user runs the application to render the scene with antialiasing applied, reducing jag edges and improving image quality. The user can specify the number of rays per pixel through the terminal.

**Why this priority**: Improves visual quality by addressing aliasing artifacts, demonstrating progressive refinement of the rendering pipeline.

**Independent Test**: Can be fully tested by running the application with antialiasing enabled and comparing the output to the non-antialiased version to verify reduced jag edges.

**Acceptance Scenarios**:

1. **Given** the scene with Phong shading, **When** the user enables antialiasing with N rays per pixel, **Then** the output image shows smoother edges compared to the non-antialiased version
2. **Given** antialiasing is enabled, **When** the user specifies a custom number of rays per pixel via terminal, **Then** the renderer uses that sample count for supersampling

---

### User Story 4 - Render with Area Light (Priority: P4)

The user runs the application to render the scene with an area light source instead of a point light, producing softer shadows. The user can specify the number of light source samples via the terminal.

**Why this priority**: Introduces area lighting, a more realistic light source model that produces soft shadows and more natural illumination.

**Independent Test**: Can be fully tested by running the application with area light enabled and verifying the output shows softer shadow edges compared to the point light shadow.

**Acceptance Scenarios**:

1. **Given** the scene with antialiasing, **When** the user enables area light with specified light samples, **Then** the rendered image shows soft shadows with gradual falloff
2. **Given** area light is active, **When** the user specifies the number of light rays via terminal, **Then** that sample count is used for shadow ray generation

---

### User Story 5 - Render with Uniform Sampling and Ellipsoid (Priority: P5)

The user runs the application to render the scene with uniform sampling for area light and replaces the sphere with an ellipsoid. All calculations remain in local coordinates transformed to global coordinates.

**Why this priority**: Completes the progressive rendering sequence with uniform sampling (improving area light quality) and demonstrates geometric flexibility by rendering an ellipsoid.

**Independent Test**: Can be fully tested by running the application with uniform sampling and ellipsoid geometry, verifying soft shadow quality improvement and correct ellipsoid rendering.

**Acceptance Scenarios**:

1. **Given** the scene with area light, **When** the user enables uniform sampling for light rays, **Then** the soft shadows show more uniform distribution and reduced noise
2. **Given** uniform sampling is active, **When** the scene includes an ellipsoid instead of a sphere, **Then** the ellipsoid is correctly rendered with proper intersection calculations in local coordinates
3. **Given** the user specifies both film rays and light rays via terminal, **Then** both sample counts are applied correctly to the rendering

---

### Edge Cases

- What happens when the user specifies zero or negative rays per pixel?
- How does the system handle ray counts that result in excessive rendering times (e.g., 1000+ rays per pixel)?
- What happens when a ray misses all objects in the scene?
- How does the system handle objects positioned behind the camera or outside the view frustum?
- What happens when the ellipsoid has extreme axis ratios (very flat or very elongated)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST render a scene containing a plane and a sphere/ellipsoid using a pinhole camera model
- **FR-002**: System MUST output a 512x512 pixel image
- **FR-003**: System MUST support progressive rendering in 5 incremental steps, where each step adds or improves upon the previous rendering
- **FR-004**: Step 1 MUST render with a single point light source, red-colored sphere (no material model), and no shadow calculations
- **FR-005**: Step 2 MUST render with shadow calculations and the Phong illumination model
- **FR-006**: Step 3 MUST render with antialiasing enabled
- **FR-007**: Step 4 MUST render with an area light source
- **FR-008**: Step 5 MUST render with uniform sampling for area light and an ellipsoid geometry
- **FR-009**: System MUST perform all intersection and shading calculations in local coordinates, then transform to global coordinates
- **FR-010**: System MUST accept terminal input for the number of rays per pixel (film rays)
- **FR-011**: System MUST accept terminal input for the number of light source samples (light rays)
- **FR-012**: System MUST allow the user to select the rendering step/stage via terminal input
- **FR-013**: System MUST apply the Phong illumination model with ambient, diffuse, and specular components in steps 2 and beyond
- **FR-014**: System MUST cast primary rays through each pixel of the 512x512 film plane
- **FR-015**: System MUST cast shadow rays toward light sources for shadow calculations

### Key Entities

- **Pinhole Camera**: Defines the viewing model with a single viewpoint, projecting rays through each pixel of the 512x512 film plane
- **Sphere**: A geometric primitive with position, radius, and surface properties (red color in step 1, Phong material in steps 2+)
- **Ellipsoid**: A geometric primitive with three axis scales, position, and surface properties, rendered in step 5
- **Plane**: An infinite flat geometric surface serving as the ground plane in the scene
- **Point Light**: A zero-dimensional light source emitting equally in all directions, used in steps 1-3
- **Area Light**: A two-dimensional light source with finite extent, producing soft shadows, used in steps 4-5
- **Ray**: A line segment defined by an origin and direction, cast from the camera through pixels (primary rays) or from surface points toward lights (shadow rays)
- **Film**: The 512x512 pixel grid where the final image is accumulated

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Each of the 5 rendering steps produces a valid 512x512 pixel image file
- **SC-002**: Progressive rendering is verifiable - each step's output image shows visible improvement over the previous step
- **SC-003**: User can specify rays per pixel via terminal and observe the effect on image quality (antialiasing and area light sampling)
- **SC-004**: User can specify light source sample count via terminal and observe the effect on shadow softness and noise
- **SC-005**: Step 1 image shows a red sphere on a plane with point light illumination and hard shadow boundaries
- **SC-006**: Step 2 image shows Phong-shaded sphere with visible shadows cast by objects
- **SC-007**: Step 3 image shows visibly smoother edges compared to step 2 (reduced aliasing artifacts)
- **SC-008**: Step 4 image shows soft shadows with gradual falloff at shadow boundaries
- **SC-009**: Step 5 image shows an ellipsoid geometry with improved uniform sampling quality
- **SC-010**: All ray intersection calculations are performed in local object coordinates and correctly transformed to global coordinates

## Assumptions

- Users have Python 3.x installed on their system
- The application runs from the command line and does not require a GUI for parameter input
- Output images are saved in a common format (e.g., PNG or PPM) to the local filesystem
- A reasonable default number of rays per pixel (e.g., 1 for non-antialiased, 4 for antialiased) is used when not specified
- A reasonable default number of light samples (e.g., 1 for point light, 16 for area light) is used when not specified
- The scene (camera position, object positions, light positions) uses predefined default values that produce a visually meaningful image
- Target platform is desktop (macOS, Linux, or Windows)
- No real-time rendering is required - offline rendering with reasonable completion time (seconds to minutes) is acceptable
