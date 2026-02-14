<div align="center">

<img src="/docs/logo.webp" alt="NeoVideoLingo Logo" height="140">

# Conectando cada fotograma del mundo

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

Versión basada en desarrollo secundario de [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo).  
Para ver las funciones completas y la documentación originales, visite el [repositorio original](https://github.com/Huanshere/VideoLingo).

## Introducción
NeoVideoLingo: herramienta de localización de video de alta calidad todo en uno

🎥 Procesamiento inteligente: integración de yt-dlp para descargar, reconocimiento WhisperX / Parakeet, segmentación precisa de subtítulos mediante algoritmos NLP.

📝 Traducción perfecta:采用"traducción literal-reflexión-traducción interpretativa" proceso de tres pasos, combinado con biblioteca de términos personalizados, rechazando la sensación de traducción mecánica.

✅ Experiencia visual: cumplimiento estricto de los estándares de subtítulos de Netflix, asegurando que cada frase se muestre en una sola línea, lectura sin estrés.

🗣️ Síntesis de voz: soporte para indextts2.0 próximamente.

🚀 Operación conveniente: interfaz Streamlit con inicio de un solo clic, registro completo del proceso, soporte para interrupción y recuperación en cualquier momento.

## Soporte de idiomas
Soporte de idiomas de entrada:

🇨🇳 Chino | 🇺🇸 Inglés | 🇷🇺 Ruso | 🇫🇷 Francés | 🇩🇪 Alemán | 🇮🇹 Italiano | 🇪🇸 Español | 🇯🇵 Japonés | 🇧🇬 Búlgaro | 🇭🇷 Croata | 🇨🇿 Checo | 🇩🇰 Danés | 🇳🇱 Holandés | 🇪🇪 Estonio | 🇫🇮 Finlandés | 🇬🇷 Griego | 🇭🇺 Húngaro | 🇱🇻 Letón | 🇱🇹 Lituano | 🇲🇹 Maltés | 🇵🇱 Polaco | 🇵🇹 Portugués | 🇷🇴 Rumano | 🇸🇰 Eslovaco | 🇸🇮 Esloveno | 🇸🇪 Sueco | 🇺🇦 Ucraniano

## Actualizaciones recientes

Enero 2026
- Actualización de dependencias - incluyendo la versión antigua de av que causaba errores previamente
- Optimización del script de instalación automática de dependencias
- Actualización del método de configuración de ancho/icono en Streamlit
- Añadida función para obtener modelos disponibles
- Mantenimiento automático de archivos de traducción
- Modificación del color de fuente de los botones
- Interruptor RoFormer en barra lateral
- Actualizado a la última versión de WhisperX
- Reemplazado Demucs con BS-RoFormer

Diciembre 2025
- Ocultar barra de progreso al descargar YouTube
- Corrección de errores de ruta

Noviembre 2025
- Corrección de errores de ruta
- Corrección de error de división por dos puntos
- Corrección de imagen de portada
- Activación del modo headless

Octubre 2025
- Corrección de problema de alineación fallida
- Soporte para transcripción Parakeet
**https://github.com/lost0427/parakeet-api-vl**

Septiembre 2025
- Corrección de archivo en history
- Actualización de ajustes de parámetros WhisperX
- Actualización de palabras clave de prompts
- Proxy de imagen de portada
- Visualización de portadas estándar y máximas
- Corrección de problema de color de fondo de metadata
- Procesamiento de youtube shorts
- Script de servicio para Windows
- Parámetros VAD personalizados
- Conversión de tiempo de publicación
- Modificaciones de estilo de imágenes y texto
- Botón de descarga de video
- Soporte para youtu.be
- Limpieza de enlaces de YouTube
- Actualización de traducciones de opciones
- Interruptor para mostrar información de videos de YouTube
- Interruptor opcional para descargar h264 (mp4)
- Mostrar información de video y portada de YouTube
- Prevención de ejecución múltiple de WhisperX
- Prevención de errores causados por ejecución múltiple de demucs
- Archivo de ejemplo de configuración para autenticación multiusuario
- Añadido sistema de inicio de sesión de usuarios, soporte multiusuario completado parcialmente

## Nota

Este repositorio no mantiene la parte de doblaje

## Método de instalación

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```