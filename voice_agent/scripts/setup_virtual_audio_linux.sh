#!/usr/bin/env bash
# Configura un dispositivo de audio virtual en Linux (PulseAudio)
# para enrutar la voz del agente directamente al micrófono de Zoom.
#
# Uso: bash scripts/setup_virtual_audio_linux.sh
# Luego en Zoom: Configuración → Audio → Micrófono → "VirtualMic"

set -e

echo "=== Configurando audio virtual para Zoom en Linux ==="

# Crea sink virtual (altavoz virtual)
pactl load-module module-null-sink sink_name=VirtualSpeaker sink_properties=device.description=VirtualSpeaker

# Crea source virtual a partir del monitor del sink (esto es el "micrófono virtual")
pactl load-module module-virtual-source source_name=VirtualMic \
    master=VirtualSpeaker.monitor \
    source_properties=device.description=VirtualMic

echo ""
echo "✓ Dispositivo virtual creado:"
echo "  - Salida (para el agente): VirtualSpeaker"
echo "  - Entrada (para Zoom):    VirtualMic"
echo ""
echo "Pasos siguientes:"
echo "1. En Zoom → Configuración → Audio → Micrófono → selecciona 'VirtualMic'"
echo "2. En config.yaml → audio.output_device → pon 'VirtualSpeaker'"
echo ""
echo "Para hacer permanente, agrega estas líneas a /etc/pulse/default.pa:"
echo "  load-module module-null-sink sink_name=VirtualSpeaker"
echo "  load-module module-virtual-source source_name=VirtualMic master=VirtualSpeaker.monitor"
