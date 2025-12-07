import streamlit as st
import json
from datetime import datetime, date

# Configuración de la página
st.set_page_config(page_title="Datos del Productor", page_icon="🌾", layout="wide")

st.title("🌾 Datos del Productor")
st.markdown("---")

# Inicializar session_state si no existe
if 'datos_productor' not in st.session_state:
    st.session_state.datos_productor = {}

# Crear columnas para organizar mejor el formulario
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Información General")
    
    nombre_productor = st.text_input(
        "Nombre del Productor",
        value=st.session_state.datos_productor.get('nombre_productor', ''),
        help="Ingrese su nombre completo"
    )
    
    ubicacion = st.selectbox(
        "Departamento / Región",
        options=[
            "Seleccionar...",
            "Lima", "Arequipa", "La Libertad", "Lambayeque", 
            "Piura", "Ica", "Junín", "Cajamarca", "Cusco",
            "Ancash", "Ayacucho", "Huánuco", "San Martín"
        ],
        index=0 if not st.session_state.datos_productor.get('ubicacion') 
              else ["Seleccionar...", "Lima", "Arequipa", "La Libertad", "Lambayeque", 
                    "Piura", "Ica", "Junín", "Cajamarca", "Cusco",
                    "Ancash", "Ayacucho", "Huánuco", "San Martín"].index(
                        st.session_state.datos_productor.get('ubicacion', 'Seleccionar...')
                    )
    )
    
    area_disponible = st.number_input(
        "Área Disponible (hectáreas)",
        min_value=0.1,
        max_value=1000.0,
        value=st.session_state.datos_productor.get('area_disponible', 5.0),
        step=0.5,
        help="Área total disponible para el cultivo"
    )
    
    tipo_cultivo = st.selectbox(
        "Tipo de Cultivo",
        options=[
            "Seleccionar...",
            "Maíz", "Papa", "Arroz", "Trigo", "Quinua",
            "Espárrago", "Palta", "Café", "Cacao", "Algodón"
        ],
        index=0 if not st.session_state.datos_productor.get('tipo_cultivo') 
              else ["Seleccionar...", "Maíz", "Papa", "Arroz", "Trigo", "Quinua",
                    "Espárrago", "Palta", "Café", "Cacao", "Algodón"].index(
                        st.session_state.datos_productor.get('tipo_cultivo', 'Seleccionar...')
                    )
    )

with col2:
    st.subheader("📅 Cronograma de Campaña")
    
    fecha_siembra = st.date_input(
        "Fecha Estimada de Siembra",
        value=st.session_state.datos_productor.get('fecha_siembra', date.today()),
        help="Fecha en la que planea iniciar la siembra"
    )
    
    fecha_cosecha = st.date_input(
        "Fecha Estimada de Cosecha",
        value=st.session_state.datos_productor.get('fecha_cosecha', date.today()),
        help="Fecha estimada para la cosecha"
    )
    
    duracion_dias = (fecha_cosecha - fecha_siembra).days
    st.info(f"📊 Duración de la campaña: **{duracion_dias} días**")
    
    precio_venta_esperado = st.number_input(
        "Precio de Venta Esperado (S/. por kg)",
        min_value=0.1,
        max_value=100.0,
        value=st.session_state.datos_productor.get('precio_venta_esperado', 2.5),
        step=0.1,
        help="Precio estimado al que venderá su producto"
    )

st.markdown("---")
st.subheader("💰 Costos de Producción")

col3, col4, col5 = st.columns(3)

with col3:
    costo_mano_obra = st.number_input(
        "Mano de Obra (S/.)",
        min_value=0.0,
        value=st.session_state.datos_productor.get('costo_mano_obra', 5000.0),
        step=100.0
    )
    
    costo_semillas = st.number_input(
        "Semillas/Plantones (S/.)",
        min_value=0.0,
        value=st.session_state.datos_productor.get('costo_semillas', 1500.0),
        step=100.0
    )

with col4:
    costo_fertilizantes = st.number_input(
        "Fertilizantes (S/.)",
        min_value=0.0,
        value=st.session_state.datos_productor.get('costo_fertilizantes', 2000.0),
        step=100.0
    )
    
    costo_agua = st.number_input(
        "Agua/Riego (S/.)",
        min_value=0.0,
        value=st.session_state.datos_productor.get('costo_agua', 800.0),
        step=100.0
    )

with col5:
    costo_maquinaria = st.number_input(
        "Maquinaria (S/.)",
        min_value=0.0,
        value=st.session_state.datos_productor.get('costo_maquinaria', 3000.0),
        step=100.0
    )
    
    otros_costos = st.number_input(
        "Otros Costos (S/.)",
        min_value=0.0,
        value=st.session_state.datos_productor.get('otros_costos', 1000.0),
        step=100.0
    )

# Calcular costo total
costo_total = (costo_mano_obra + costo_semillas + costo_fertilizantes + 
               costo_agua + costo_maquinaria + otros_costos)

st.markdown("---")
st.subheader("📊 Resumen de Costos")

col6, col7, col8 = st.columns(3)
with col6:
    st.metric("Costo Total", f"S/. {costo_total:,.2f}")
with col7:
    st.metric("Costo por Hectárea", f"S/. {costo_total/area_disponible:,.2f}")
with col8:
    if duracion_dias > 0:
        st.metric("Costo Diario", f"S/. {costo_total/duracion_dias:,.2f}")

st.markdown("---")

# Botón para guardar datos
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    if st.button("💾 Guardar Datos", type="primary", use_container_width=True):
        if ubicacion == "Seleccionar..." or tipo_cultivo == "Seleccionar...":
            st.error("⚠️ Por favor complete todos los campos obligatorios")
        elif fecha_cosecha <= fecha_siembra:
            st.error("⚠️ La fecha de cosecha debe ser posterior a la fecha de siembra")
        else:
            # Guardar datos en session_state
            st.session_state.datos_productor = {
                'nombre_productor': nombre_productor,
                'ubicacion': ubicacion,
                'area_disponible': area_disponible,
                'tipo_cultivo': tipo_cultivo,
                'fecha_siembra': fecha_siembra,
                'fecha_cosecha': fecha_cosecha,
                'duracion_dias': duracion_dias,
                'precio_venta_esperado': precio_venta_esperado,
                'costo_mano_obra': costo_mano_obra,
                'costo_semillas': costo_semillas,
                'costo_fertilizantes': costo_fertilizantes,
                'costo_agua': costo_agua,
                'costo_maquinaria': costo_maquinaria,
                'otros_costos': otros_costos,
                'costo_total': costo_total,
                'fecha_registro': datetime.now().isoformat()
            }
            
            # Guardar en archivo JSON
            try:
                with open('data/productor_data.json', 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.datos_productor, f, 
                             ensure_ascii=False, indent=4, default=str)
                st.success("✅ Datos guardados exitosamente!")
                st.balloons()
            except Exception as e:
                st.warning(f"⚠️ Datos guardados en sesión pero no en archivo: {e}")

# Mostrar datos guardados si existen
if st.session_state.datos_productor:
    with st.expander("📋 Ver Datos Guardados"):
        st.json(st.session_state.datos_productor)