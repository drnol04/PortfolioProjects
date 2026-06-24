# Audio Virtual para Windows (VB-Cable)

## Instalación

1. Descarga **VB-CABLE** gratis desde: https://vb-audio.com/Cable/
2. Instala como administrador y reinicia
3. Ahora tendrás dos dispositivos nuevos:
   - `CABLE Input` (altavoz virtual — aquí envía el agente su voz)
   - `CABLE Output` (micrófono virtual — esto usa Zoom)

## Configuración en Zoom

1. Abre Zoom → Configuración → Audio
2. **Micrófono**: selecciona `CABLE Output (VB-Audio Virtual Cable)`
3. **Altavoz**: déjalo como tu altavoz normal (para escuchar la reunión)

## Configuración en config.yaml

```yaml
audio:
  output_device: "CABLE Input"   # El agente habla aquí
  input_device: null              # Micrófono real para escuchar la reunión
```

## Escuchar la reunión Y el agente al mismo tiempo

Para oírte a ti mismo por los altavoces mientras el agente usa VB-Cable:

1. Panel de Control → Sonido → Grabación
2. Clic derecho en `CABLE Output` → Propiedades
3. Pestaña "Escuchar" → activa "Escuchar este dispositivo"
4. Selecciona tu altavoz como dispositivo de reproducción

## Flujo completo

```
Reunión Zoom                     Tu computadora
┌──────────┐    audio de          ┌─────────────┐
│          │◄── participantes ─── │ Micrófono   │
│   Zoom   │                      │ real tuyo   │
│          │                      └─────────────┘
│ Micro:   │    voz del            ┌─────────────┐
│ CABLE    │◄── agente ─────────── │  Agente de  │
│ Output   │                      │    Voz      │
└──────────┘                      │  (VB-Cable  │
                                  │   Input)    │
                                  └─────────────┘
```
