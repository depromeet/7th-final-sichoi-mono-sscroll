import axios from 'axios';
import { action, observable } from 'mobx';
import ItemModel from './model';

class ItemStore {
  @observable
  itemList: ItemModel[];

  isLoading: boolean;

  constructor() {
    this.isLoading = false;
    this.itemList = [];
  }

  @action.bound
  async fetch() {
    if (this.isLoading) {
      return;
    }

    this.isLoading = true;
    const response = await axios.get('/content');
    this.isLoading = false;
    const data = response.data;

    const item = new ItemModel({ ...data });
    this.itemList.push(item);
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
