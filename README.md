# 🚀 PortLife — Portafolio Profesional de Ingeniería Informática

![PortLife Logo](assets/logo.png)

**PortLife** es el portafolio profesional web de **Juan Miguel Duarte Castañeda**, estudiante de **Ingeniería Informática**. Está desarrollado bajo estándares web modernos (**HTML5 semántico**, **CSS3 personalizado**, **JavaScript vanilla** y **Bootstrap 5**), enfocado en una arquitectura 100% estática, ligera, responsive y compatible tanto con apertura directa local como con **GitHub Pages**.

---

## 📋 Secciones del Portafolio (Requisitos Académicos)

El portafolio integra de manera estructurada las 5 secciones solicitadas:

1. **Información Personal (Hero y Sobre Mí):** Identidad, documento de identidad, edad, ubicación, carrera universitaria, semestre actual, biografía y objetivos profesionales.
2. **Estudios Realizados:** Línea de tiempo académica formal (*Ingeniería Informática*, *Tecnología en Análisis y Desarrollo de Software*, y *Diplomado en Desarrollo Backend con Python & Flask*).
3. **Proyectos Desarrollados:** Fichas interactivas con capturas, etiquetas de tecnologías, estado de avance (*GlucoKids*, *PetCare*, *Hablemos*), filtros por categoría y modal con descripción técnica completa.
4. **Lenguajes y Tecnologías:** Clasificación por categorías (*Frontend*, *Backend*, *Bases de Datos*, *Herramientas*) con niveles cualitativos y barras de progreso animadas.
5. **Áreas de Interés Profesional:** Áreas clave de profundización (*Desarrollo Web Full Stack*, *Inteligencia Artificial y Datos*, *Automatización de Procesos*, *Creación de Aplicaciones de Impacto*).

Además, cuenta con una sección de **Contacto** con canales directos (Email, GitHub, LinkedIn) y un formulario interactivo con validación en frontend.

---

## 📂 Estructura de Archivos

El proyecto cuenta con una estructura limpia, desacoplada de servidores backend o bases de datos locales:

```text
PortLife/
├── index.html          # Estructura principal y contenido completo del portafolio
├── style.css           # Estilos visuales personalizados (Cyber Navy & Cyan) y diseño responsive
├── script.js           # Lógica interactiva (modal dinámico sin fetch, filtros y animaciones)
├── assets/             # Recursos multimedia locales (logo, avatar y capturas de proyectos)
│   ├── logo.png
│   ├── student_avatar.jpg
│   ├── glucokids.jpg
│   ├── petcare.jpg
│   └── hablemos.jpg
├── .gitignore          # Reglas de exclusión de Git
└── README.md           # Documentación e instrucciones
```

---

## ⚡ ¿Cómo abrir la página directamente (Local)?

No requiere instalar Python, Flask, Node.js ni bases de datos:

1. Ve a la carpeta del proyecto `PortLife`.
2. Haz **doble clic** sobre el archivo `index.html`.
3. Se abrirá inmediatamente en tu navegador preferido (Google Chrome, Edge, Firefox, Brave, etc.) mediante el protocolo local `file:///`.

> **Nota de conectividad:** Se requiere acceso a Internet para cargar las tipografías de *Google Fonts*, la librería *Bootstrap 5* y los iconos de *Bootstrap Icons* servidos a través de CDN.

---

## 🌐 Publicación en GitHub Pages

Para publicar este portafolio en la web de forma gratuita con GitHub Pages:

1. **Subir los cambios a tu repositorio en GitHub:**
   ```bash
   git add .
   git commit -m "Convertir PortLife a portafolio estático optimizado para GitHub Pages"
   git push origin main
   ```
2. **Activar GitHub Pages:**
   * Entra a tu repositorio en GitHub (`https://github.com/tu-usuario/PortLife`).
   * Haz clic en la pestaña **Settings** (Configuración).
   * En el menú lateral izquierdo, haz clic en **Pages**.
   * En la sección **Build and deployment**:
     * **Source:** Selecciona `Deploy from a branch`.
     * **Branch:** Selecciona `main` (o `master`) y carpeta `/ (root)`.
     * Haz clic en **Save** (Guardar).
3. **Listo:** En 1 o 2 minutos, GitHub te proporcionará el enlace público de tu portafolio:
   `https://tu-usuario.github.io/PortLife/`

---

## 🛠️ Tecnologías Empleadas

* **HTML5 Semántico:** Jerarquía clara, accesibilidad y metaetiquetas Open Graph / SEO.
* **CSS3:** Variables CSS personalizadas, efectos glassmorphism, gradientes cian y paleta *Deep Navy*.
* **JavaScript (ES6+):** Renderizado de modal sin dependencias de red, filtros por categoría y animaciones con `IntersectionObserver`.
* **Bootstrap 5.3.3 (CDN):** Sistema de grilla fluida y responsive para móviles, tablets y monitores.
* **Bootstrap Icons 1.11.3 (CDN):** Iconografía estándar para tecnologías y canales de contacto.
* **Google Fonts (CDN):** Fuentes modernas *Outfit* y *Plus Jakarta Sans*.

---

**Autor:** Juan Miguel Duarte Castañeda  
**Carrera:** Ingeniería Informática  
**Año:** 2026
