import { observable } from 'mobx';

interface ModelConstructor {
  id: number;
  title: string;
  content: string;
}

export default class ItemModel {
  id: number;
  @observable title: string;
  @observable content: string;

  constructor({ id, title, content }: ModelConstructor) {
    this.id = id;
    this.title = title;
    this.content = content;
  }
}
