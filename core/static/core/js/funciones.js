function eliminarUsuario(id) {
  Swal.fire({
    title: "¿Estás seguro?",
    text: "¡No podrás revertir esto!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "¡Sí, elimínalo!",
    cancelButtonText: "Cancelar",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "¡Usuario eliminado!",
        text: "El usuario ha sido eliminado.",
        icon: "success",
      }).then(() => {
        window.location.href = "/dashboard/usuarios/eliminar/" + id;
      });
    }
  });
}

function eliminarProducto(id) {
  Swal.fire({
    title: "¿Estás seguro?",
    text: "¡No podrás revertir esto!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "¡Sí, elimínalo!",
    cancelButtonText: "Cancelar",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "¡Producto eliminado!",
        text: "El producto ha sido eliminado.",
        icon: "success",
      }).then(() => {
        window.location.href = "/dashboard/productos/eliminar/" + id;
      });
    }
  });
}

function eliminarArtista(id) {
  Swal.fire({
    title: "¿Estás seguro?",
    text: "¡No podrás revertir esto!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "¡Sí, elimínalo!",
    cancelButtonText: "Cancelar",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "¡Artista eliminado!",
        text: "El artista ha sido eliminado.",
        icon: "success",
      }).then(() => {
        window.location.href = "/dashboard/artistas/eliminar/" + id;
      });
    }
  });
}




