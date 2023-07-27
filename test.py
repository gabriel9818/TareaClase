import geocoder

def obtener_ubicacion_actual():
    ubicacion = geocoder.ip('me')
    
    if ubicacion.ok:
        direccion = ubicacion.address
        latitud = ubicacion.lat
        longitud = ubicacion.lng
        print(f"Dirección: {direccion}")
        print(f"Latitud: {latitud}")
        print(f"Longitud: {longitud}")
    else:
        print("No se pudo obtener la ubicación actual.")

if __name__ == "__main__":
    obtener_ubicacion_actual()


