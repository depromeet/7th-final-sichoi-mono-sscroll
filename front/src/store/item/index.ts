import axios from 'axios';
import { action, observable } from 'mobx';
import ItemModel, { ModelConstructor } from './model';

class ItemStore {
  @observable
  itemList: ItemModel[];

  isLoading: boolean;

  constructor() {
    this.isLoading = false;
    this.itemList = [];
  }

  @action.bound
  async fetchById(id: string) {
    if (this.isLoading) {
      return;
    }
    this.isLoading = true;
    const res = await axios.get<ModelConstructor>(`/content/${id}`);
    this.isLoading = false;
    this.itemList.push(new ItemModel({ ...res.data }));
  }

  @action.bound
  async fetch() {
    if (this.isLoading) {
      return;
    }

    this.isLoading = true;
    const response = await axios.get<ModelConstructor[]>('/content');
    this.isLoading = false;
    const data = response.data;

    data.forEach(el => {
      const item = new ItemModel({ ...el });
      const findItem = this.itemList.find(el => el.id === item.id);
      if (findItem) {
        return;
      }
      this.itemList.push(item);
    });
  }

  async read(id: number) {
    await axios.post(`/content/${id}/read`);
  }
}

export default new ItemStore();

/**
 * Item에 들어갈 것
 * created_at
 * view count
 * title
 * description
 * like unlike
 */
