import { resolveServiceURL } from "./resolve-service-url";
import type { Datastore } from "../datastore/types";

export function listDatastores() {
  return fetch(resolveServiceURL("datastores"), { method: "GET" })
    .then((res) => res.json())
    .then((res) => res.datastores as Datastore[]);
}

export function createDatastore(name: string, files: File[]) {
  const form = new FormData();
  form.append("name", name);
  files.forEach((f) => form.append("files", f));
  return fetch(resolveServiceURL("datastores"), {
    method: "POST",
    body: form,
  }).then((res) => res.json());
}
