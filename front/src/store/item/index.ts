import axios from 'axios';
import { action, observable } from 'mobx';
import ItemModel, { ModelConstructor } from './model';
import ReactGA from 'react-ga';

class ItemStore {
  @observable
  itemList: ItemModel[] = [];

  @observable
  readItemList: number[] = [];

  isLoading: boolean = false;

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
      if (!findItem) {
        this.itemList.push(item);
      }
    });
  }

  async read(id: number) {
    if (this.readItemList.find(el => el === id)) {
      return;
    }
    await axios.post(`/content/${id}/read`);
    ReactGA.pageview('/' + id);
    this.readItemList.push(id);
  }
}

export default new ItemStore();
