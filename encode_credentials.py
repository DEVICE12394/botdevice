"""
Script para codificar credenciales de Google Service Account a Base64
Útil para despliegue en producción o Docker
"""
import base64
import json
import os


def encode_json_file_to_base64(json_file_path):
    """
    Convierte un archivo JSON a Base64
    
    Args:
        json_file_path: Ruta al archivo JSON de credenciales
        
    Returns:
        String en Base64
    """
    try:
        # Leer el archivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
        
        # Validar que sea JSON válido
        json.loads(json_content)
        
        # Codificar a Base64
        base64_encoded = base64.b64encode(
            json_content.encode('utf-8')
        ).decode('utf-8')
        
        return base64_encoded
    
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{json_file_path}'")
        return None
    except json.JSONDecodeError:
        print("❌ Error: El archivo no contiene JSON válido")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None


def decode_base64_to_json(base64_string, output_file=None):
    """
    Decodifica un string Base64 a JSON
    
    Args:
        base64_string: String codificado en Base64
        output_file: (Opcional) Ruta donde guardar el JSON
        
    Returns:
        Diccionario con el contenido JSON
    """
    try:
        # Decodificar desde Base64
        decoded_bytes = base64.b64decode(base64_string)
        decoded_string = decoded_bytes.decode('utf-8')
        
        # Parsear JSON
        json_data = json.loads(decoded_string)
        
        # Guardar a archivo si se especifica
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            print(f"✅ JSON guardado en: {output_file}")
        
        return json_data
    
    except Exception as e:
        print(f"❌ Error al decodificar: {e}")
        return None


def main():
    """Función principal interactiva"""
    print("=" * 60)
    print("🔐 Codificador/Decodificador de Credenciales Google")
    print("=" * 60)
    print()
    print("Selecciona una opción:")
    print("1. Codificar archivo JSON a Base64")
    print("2. Decodificar Base64 a JSON")
    print("3. Salir")
    print()
    
    choice = input("Opción (1/2/3): ").strip()
    
    if choice == "1":
        print("\n--- Codificar JSON a Base64 ---")
        json_file = input(
            "Ruta al archivo JSON (o presiona Enter para "
            "'credentials.json'): "
        ).strip()
        
        if not json_file:
            json_file = "credentials.json"
        
        # Buscar en el directorio actual si no es ruta absoluta
        if not os.path.isabs(json_file):
            json_file = os.path.join(os.getcwd(), json_file)
        
        print(f"\n📂 Buscando: {json_file}")
        base64_result = encode_json_file_to_base64(json_file)
        
        if base64_result:
            print("\n✅ ¡Codificación exitosa!")
            print("\n" + "=" * 60)
            print("📋 Copia este valor para GOOGLE_SERVICE_ACCOUNT_JSON:")
            print("=" * 60)
            print(base64_result)
            print("=" * 60)
            
            # Guardar en archivo
            save = input(
                "\n¿Guardar en un archivo? (s/n): "
            ).strip().lower()
            if save == 's':
                output_file = "credentials_base64.txt"
                with open(output_file, 'w') as f:
                    f.write(base64_result)
                print(f"✅ Guardado en: {output_file}")
    
    elif choice == "2":
        print("\n--- Decodificar Base64 a JSON ---")
        base64_input = input(
            "Pega el string Base64: "
        ).strip()
        
        output_file = input(
            "¿Guardar a archivo? (deja vacío para solo mostrar): "
        ).strip()
        
        if not output_file:
            output_file = None
        
        json_result = decode_base64_to_json(base64_input, output_file)
        
        if json_result:
            print("\n✅ ¡Decodificación exitosa!")
            print("\n" + "=" * 60)
            print("📋 Contenido JSON:")
            print("=" * 60)
            print(json.dumps(json_result, indent=2))
            print("=" * 60)
    
    elif choice == "3":
        print("\n👋 ¡Hasta luego!")
    
    else:
        print("\n❌ Opción inválida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada")
    except Exception as e:
        print(f"\n❌ Error: {e}")
