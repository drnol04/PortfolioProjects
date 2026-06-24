#!/usr/bin/env bash
# Instrucciones para audio virtual en macOS con BlackHole
# https://github.com/ExistentialAudio/BlackHole

echo "=== Audio Virtual para macOS ==="
echo ""
echo "1. Instala BlackHole 2ch:"
echo "   brew install blackhole-2ch"
echo "   O descarga desde: https://existential.audio/blackhole/"
echo ""
echo "2. Abre 'Audio MIDI Setup' (en Aplicaciones → Utilidades)"
echo "   - Crea un 'Multi-Output Device' que incluya:"
echo "     ✓ BlackHole 2ch"
echo "     ✓ Altavoces internos (para escucharte tú también)"
echo ""
echo "3. En Zoom → Configuración → Audio:"
echo "   - Altavoz: Multi-Output Device"
echo "   - Micrófono: BlackHole 2ch"
echo ""
echo "4. En config.yaml:"
echo "   audio.output_device: 'BlackHole 2ch'"
echo ""
echo "Con esto el agente habla por BlackHole y Zoom lo recibe como micrófono."
