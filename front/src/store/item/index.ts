import axios from 'axios';
import { action, observable } from 'mobx';
import ItemModel from './model';

class ItemStore {
  @observable
  itemList: ItemModel[];

  id: number;

  constructor() {
    this.id = 0;
    this.itemList = [];
  }

  @action.bound
  async fetch() {
    const response = await axios.get('/content');
    const data = response.data;

    const item = new ItemModel(data.id, data.title, data.body);
    this.itemList.push(item);
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
