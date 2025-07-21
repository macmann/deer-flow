import { create } from "zustand";
import type { Datastore } from "../datastore/types";
import { listDatastores } from "../api/datastore";

export const useDatastoreStore = create<{ datastores: Datastore[] }>(() => ({
  datastores: [],
}));

export async function loadDatastores() {
  const res = await listDatastores();
  useDatastoreStore.setState({ datastores: res });
}
