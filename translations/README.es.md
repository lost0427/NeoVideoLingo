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

📝 Traducción perfecta: proceso de tres pasos "traducción literal-reflexión-traducción interpretativa", combinado con biblioteca de términos personalizados, rechazando la sensación de traducción mecánica.

✅ Experiencia visual: cumplimiento estricto de los estándares de subtítulos de Netflix, asegurando que cada frase se muestre en una sola línea, lectura sin estrés.

🗣️ Síntesis de voz: soporte para indextts2.0 próximamente.

🚀 Operación conveniente: interfaz Streamlit con inicio de un solo clic, registro completo del proceso, soporte para interrupción y recuperación en cualquier momento.

## Soporte de idiomas
Soporte de idiomas de entrada:

🇨🇳 Chino | 🇺🇸 Inglés | 🇷🇺 Ruso | 🇫🇷 Francés | 🇩🇪 Alemán | 🇮🇹 Italiano | 🇪🇸 Español | 🇯🇵 Japonés | 🇧🇬 Búlgaro | 🇭🇷 Croata | 🇨🇿 Checo | 🇩🇰 Danés | 🇳🇱 Holandés | 🇪🇪 Estonio | 🇫🇮 Finlandés | 🇬🇷 Griego | 🇭🇺 Húngaro | 🇱🇻 Letón | 🇱🇹 Lituano | 🇲🇹 Maltés | 🇵🇱 Polaco | 🇵🇹 Portugués | 🇷🇴 Rumano | 🇸🇰 Eslovaco | 🇸🇮 Esloveno | 🇸🇪 Sueco | 🇺🇦 Ucraniano | 🇭🇰 Cantonés | 🇸🇦 Árabe | 🇮🇩 Indonesio | 🇰🇷 Coreano | 🇹🇭 Tailandés | 🇻🇳 Vietnamita | 🇹🇷 Turco | 🇮🇳 Hindi | 🇲🇾 Malay | 🇵🇭 Filipino | 🇮🇷 Persa | 🇲🇰 Macedonio

Soporte de dialectos:
Anhui, Nordeste, Fujian, Gansu, Guizhou, Hebei, Henan, Hubei, Hunan, Jiangxi, Ningxia, Shandong, Shaanxi, Shanxi, Sichuan, Tianjin, Yunnan, Zhejiang, Cantonés (Hong Kong), Cantonés (Guangdong), Wu, Minnan

## Tutorial de instalación de Qwen3ASR
Según la guía oficial:

"Para facilitar el uso de nuestro paquete Python qwen-asr, proporcionamos una imagen Docker preconstruida: qwenllm/qwen3-asr. Solo necesita instalar los controladores de GPU y descargar los archivos del modelo para ejecutar el código. Siga la guía de instalación de NVIDIA Container Toolkit para asegurar que Docker pueda acceder a su GPU. Si se encuentra en China continental y no puede conectarse a Docker Hub, puede utilizar el caché de imagen para acelerar la descarga de la imagen."

En Windows, instale Docker, cree un archivo .ps1 o ingréselo directamente en PowerShell:

```
$LOCAL_WORKDIR = "F:\Docker\qwen3asr"
$HOST_PORT = 8700
$CONTAINER_PORT = 80
docker run --gpus all --name qwen3-asr `
    -v /var/run/docker.sock:/var/run/docker.sock `
    -p "${HOST_PORT}:${CONTAINER_PORT}" `
    --mount "type=bind,source=${LOCAL_WORKDIR},target=/data/shared/Qwen3-ASR" `
    --shm-size=4gb `
    -it qwenllm/qwen3-asr:latest
```
Si encuentra problemas de red, puede intentar usar

docker.1ms.run/qwenllm/qwen3-asr

Después de descargar y arrancar exitosamente el contenedor, el servicio de transcripción no se iniciará automáticamente, consulte el archivo de este proyecto

\core\all_whisper_methods\qwenasrvl.py

```
#vim /usr/local/bin/qwenasrvl
#chmod +x /usr/local/bin/qwenasrvl
#qwenasrvl
```
Siga las indicaciones para escribir el archivo y otorgar permisos, luego ejecútelo. Usa el marco vllm, ejecutándose en el puerto 80 del contenedor (puerto 8700 del host).

## Actualizaciones recientes
Febrero 2026
- Uso de Pydantic
- Eliminación de TTS de pago
- Optimización de traducción y herramientas de traducción automática, añadido botón para reiniciar al primer paso
- Actualización del nuevo método de transcripción de idiomas Qwen3ASR
(Qwen3-ASR-1.7B + Qwen3-ForcedAligner-0.6B)
https://github.com/QwenLM/Qwen3-ASR

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